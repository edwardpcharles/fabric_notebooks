# Welcome to a folder of random Microsoft Fabric Notebooks 

### These have varying levels of usefulness. I put them together on weekends and late nights when I got excited about something and decided to dive headfirst into it.

#### I don't even attempt to use version control for my personal stuff, so most of this folder will be randomly updated using the GitHub Web UI when I have something I want to share. That said, this folder is starting to get disorganized, so I decided to add a README to keep track of everything.

#### Projects/Files in order of initial upload:
- table_save.ipynb: A notebook that refreshes a single table in a Power BI semantic model and then writes the results to a connected lakehouse. (Needs to be redone; there are much more efficient ways to do the same thing.)

- fabric_python_demo.ipynb: A notebook where I use a few Semantic link functions: list workspaces, list datasets, list measures, and evaluate_measure

- Measure Dependency Graph Builder.ipynb: A really good idea - better executed by the team behind Semantic Link Labs. Takes a measure, and then produces a image of all the upstream and downstream measures, saves the image in the files of the attached lakehouse. 

- budget folder: A example of loading excel data into a Type 2 Table. Contains two notebooks: 1. For Creating the inital type 2 table, 2. For merging into the Type 2 Table

- Get All User Access.ipynb: A notebook that uses semantic link labs and semantic link to pull all workspace users, report users, app users, and then dataset RLS roles and assigned users. Some the code submits requests to the Power BI admin rest API.

- Get Dataset Refresh Enabled From Report.ipynb: A notebook with a python function that takes a report name, optional report workspace and then responds with T/F if the dataset refresh it hooks into is enabled.

- Get Dataset Next Refresh From Report.ipynb: A notebook with a Python function that takes a report name and an optional report workspace, then responds with the report's dataset's next scheduled refresh datetime.
  
- Get Report Dataset Details.ipynb: A notebook with two python functions one of which is modified from "Get Dataset Next Refresh From Report.ipynb" you can feed the second function a workspace name, and it will go get the refresh status of all the reports in that workspace!
  
- Re-enable Report dataset.ipynb: A notebook with a function that takes a report name and report workspace and re-enables the dataset if it is disabled.

- Get Report Usage.ipynb: A fabric notebook to grab report usage out of the power bi
  
- Final Get Report Dataset Details.ipynb: Same notebook as Get Report Dataset Details only with try + catch statements and saves to the data lake.

- Thin Report Splitter.ipynb: A Notbook that can take a report/semantic model combo in a workspace and split it into a thin report connected to a semantic model in another workspace
  
- Duplicate Semantic Model with model.bim.ipynb: A Notebook that extracts a model.bim file one semantic model and deploys it into a new one

- Github Commit.ipynb: A notebook that checks a workspace's Git commit status and commits the workspace if it hasn't been committed.

- Dax Formatter: A notbook that loops through all the measures in a semantic model and formatts them using DAX Formatter.com
  
- Grab All Metadata: loops through all the semantic models in a workspace and gets the tables, columns, and measure definition
