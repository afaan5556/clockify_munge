import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go

######################## Part 1: Read and prep combined data source ########################
# Read combined data
ROOT_DIR = '../ConsolidatedData/'
# TODO: Update preprocessing to create and overwrite a single export csv only
# TODO: Rename the path below to that single csv file name
df = pd.read_csv(ROOT_DIR + '2018823_consolidated_clockify_data.csv')
# Drop the doubled index colum
df = df.drop(columns=['Unnamed: 0'])
# Set datetime columns
df['Start Date'] = pd.to_datetime(df['Start Date'])
# Set week end date column to datetime
df['End Date'] = pd.to_datetime(df['End Date'])
# Set Time (h) to timedelta
df['Time (h)'] = pd.to_timedelta(df['Time (h)'])


######################## Part 2: Functions for data sub-sets and queries needed for visualizations ########################

# Function to get parameter filtered subset of df
def filter_param(input_df, param, param_value):
	return input_df[input_df[param] == param_value]

# Function to get parameter inverse filtered subset of df
def inverse_filter_param(input_df, param, param_value):
	return input_df[input_df[param] != param_value]

# Function to set multi-index on a param
def create_multi_index_df(input_df, set_index_list=list):
    # First sort df on the multi-index column which is first item in index list
    input_df.sort_values(by=[set_index_list[0]], inplace=True)
    # Create multi-index
    multi_df = input_df.set_index(set_index_list)
    return multi_df

# Function to sum on a multi-index df at any number of levels
def sum_df_on_mi(input_df, group_by_list=list, sum_on_list=list):
    sum_df = input_df.groupby(group_by_list)[sum_on_list].sum()
    return sum_df

######################## Part 3: Call/test functions ########################

# Get the unfiltered and filtered versions of the df
df_unfiltered = filter_param(df, 'Task', 'Unfiltered') # Base df not by task
df_filtered = inverse_filter_param(df, 'Task', 'Unfiltered') # Base df by task

# Get the project and task column based multi-index df
project_multi_df = create_multi_index_df(df, ['Project', 'Task'])
task_multi_df = create_multi_index_df(df, ['Task', 'Project'])

# Get project and task grouped absolute sum dfs
project_sum_df = sum_df_on_mi(project_multi_df, ['Project'], ['Time (h)'])
task_sum_df = sum_df_on_mi(task_multi_df, ['Task'], ['Time (h)'])

# Get project and task grouped second level sum dfs
project_task_sum_df = sum_df_on_mi(project_multi_df, ['Project', 'Task'], ['Time (h)'])
task_project_sum_df = sum_df_on_mi(task_multi_df, ['Task', 'Project'], ['Time (h)'])

