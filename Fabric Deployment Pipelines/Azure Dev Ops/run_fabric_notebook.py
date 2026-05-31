import argparse
import json
import sys
import time
from typing import Any, Dict, List, Optional

import requests
from azure.identity import AzureCliCredential

FABRIC_SCOPE = "https://api.fabric.microsoft.com/.default"
FABRIC_API_ROOT = "https://api.fabric.microsoft.com/v1"
TERMINAL_STATUSES = {"Completed", "Failed", "Cancelled", "Deduped"}


def _headers() -> Dict[str, str]:
    credential = AzureCliCredential()
    token = credential.get_token(FABRIC_SCOPE).token
    return {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }


def _run_job(
    workspace_id: str,
    item_id: str,
    job_type: str,
    parameters: Optional[List[Dict[str, Any]]],
) -> Dict[str, Any]:
    url = f"{FABRIC_API_ROOT}/workspaces/{workspace_id}/items/{item_id}/jobs/{job_type}/instances"

    payload: Dict[str, Any] = {}
    if parameters:
        payload["parameters"] = parameters

    response = requests.post(url, headers=_headers(), json=payload if payload else None, timeout=60)
    if response.status_code != 202:
        raise RuntimeError(
            f"Run request failed: HTTP {response.status_code} - {response.text}"
        )

    location = response.headers.get("Location")
    retry_after = int(response.headers.get("Retry-After", "10"))

    if not location:
        raise RuntimeError("Fabric API did not return a Location header for job polling.")

    return {"location": location, "retry_after": retry_after}


def _poll_job(location: str, initial_wait_seconds: int, timeout_seconds: int) -> Dict[str, Any]:
    start = time.time()
    wait = max(initial_wait_seconds, 1)

    time.sleep(wait)

    while True:
        response = requests.get(location, headers=_headers(), timeout=60)
        if response.status_code != 200:
            raise RuntimeError(
                f"Polling failed: HTTP {response.status_code} - {response.text}"
            )

        data = response.json()
        status = data.get("status")
        if status in TERMINAL_STATUSES:
            return data

        elapsed = time.time() - start
        if elapsed > timeout_seconds:
            raise TimeoutError(
                f"Timeout after {timeout_seconds}s. Last status: {status}"
            )

        wait = int(response.headers.get("Retry-After", "10"))
        time.sleep(max(wait, 1))


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run a Microsoft Fabric Notebook job and return input/output as JSON."
    )
    parser.add_argument("--workspace-id", required=True, help="Fabric workspace GUID")
    parser.add_argument("--item-id", required=True, help="Notebook item GUID")
    parser.add_argument(
        "--job-type",
        default="Execute",
        help="Job type for notebook runs. Default: Execute",
    )
    parser.add_argument(
        "--parameters-json",
        default="[]",
        help=(
            "JSON array of job parameters. Example: "
            "'[{\"name\":\"RunDate\",\"value\":\"2026-05-26\",\"type\":\"Text\"}]'"
        ),
    )
    parser.add_argument(
        "--timeout-seconds",
        type=int,
        default=1800,
        help="Max wait time for job completion",
    )
    args = parser.parse_args()

    try:
        parsed_parameters = json.loads(args.parameters_json)
        if not isinstance(parsed_parameters, list):
            raise ValueError("parameters-json must be a JSON array")

        run_info = _run_job(
            workspace_id=args.workspace_id,
            item_id=args.item_id,
            job_type=args.job_type,
            parameters=parsed_parameters,
        )

        result = _poll_job(
            location=run_info["location"],
            initial_wait_seconds=run_info["retry_after"],
            timeout_seconds=args.timeout_seconds,
        )

        output = {
            "input": {
                "workspace_id": args.workspace_id,
                "item_id": args.item_id,
                "job_type": args.job_type,
                "parameters": parsed_parameters,
                "timeout_seconds": args.timeout_seconds,
            },
            "output": {
                "job_instance_id": result.get("id"),
                "status": result.get("status"),
                "start_time_utc": result.get("startTimeUtc"),
                "end_time_utc": result.get("endTimeUtc"),
                "root_activity_id": result.get("rootActivityId"),
                "failure_reason": result.get("failureReason"),
                "succeeded": result.get("status") == "Completed",
            },
        }

        print(json.dumps(output, indent=2))

        if result.get("status") != "Completed":
            return 2

        return 0

    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
