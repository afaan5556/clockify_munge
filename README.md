# clockif_munge.py
This script reads standard clockify .xlsx exports in various folders and creates a combined csv with meta data that clockify does not export

## Data Required
* clockfiy .xlsx export files

## Variables
* `ROOT_DIR`: Relative path to where the folders for each clockify export report are placed. This folder is called `RawExportData` per this code base

# clockify_viz.py
This script reads the csv exported by `clockify_munge.py` and creates a dynamic dash.plot.ly  visualization

# Use
## Folder structure
Place the script in in a `Scripts` directory that is in the same root as the `RawExportData` folder

Create a `ConsolidatedData` directory in the same root. This is where the consolidated csv export will be written. 

In summary, the local folder structure should be:
* ConsolidatedData (Where the consolidated csv will be written to)
* RawDataExport (Download and store clockify .xlsx files in this folder, using subfolders if needed)
* Scripts (Place to store the `clockify_munge.py` and `clockify_viz.py` scripts)

## Running the scripts
* `python clockify_munge.py`
* `python clockify_viz.py`
* Browse to local host: http://127.0.0.1:8050/

