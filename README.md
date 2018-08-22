# clockif_munge.py
This script reads standard clockify .xlsx exports in various folders and creates a combined csv with meta data that clockify does not export

## Data Required
* clockfiy .xlsx export files

## Variables
* `ROOT_DIR`: Relative path to where the folders for each clockify export report are placed. This folder is called `RawExportData` per this code base

## Use
Place the script in in a `Scripts` directory that is in the same root as the `RawExportData` folder

Create a `ConsolidatedData` directory in the same root. This is where the consolidated csv export will be written. 

# clockif_viz.py
This script reads the csv exported by `clockify_munge.py` and creates a dynamic dash.plot.ly  visualization 