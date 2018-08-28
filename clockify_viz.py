import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
import datetime as dt
from dash.dependencies import Input, Output

######################## Part 1A: Read and prep combined data source ########################
# Constants
UNITS = {'FloorTrusses': 'bd-ft', 'RoofTrusses': 'bd-ft', 'FloorPanels': 'sq-ft', 'WallPanels': 'ln-ft'}

# Read combined data
ROOT_DIR = '../ConsolidatedData/'
df = pd.read_csv(ROOT_DIR + 'consolidated_clockify_data.csv')
# Drop the doubled index colum
df = df.drop(columns=['Unnamed: 0'])
# Set datetime columns
df['Start Date'] = pd.to_datetime(df['Start Date'])
# Set week end date column to datetime
df['End Date'] = pd.to_datetime(df['End Date'])
# Set Time (h) to timedelta
df['Time (h)'] = pd.to_timedelta(df['Time (h)'])

######################## Part 1B: Get the filtered (with tasks) and the unfiltered (all) dfs ########################

# Function to get parameter filtered subset of df
def filter_param(input_df, param, param_value):
    return input_df[input_df[param] == param_value]

# Function to get parameter inverse filtered subset of df
def inverse_filter_param(input_df, param, param_value):
    return input_df[input_df[param] != param_value]

# Get the unfiltered and filtered versions of the df
df_unfiltered = filter_param(df, 'Task', 'Unfiltered') # Base df not by task
df_filtered = inverse_filter_param(df, 'Task', 'Unfiltered') # Base df by task

df_dict = {'Data with task tags only': df_filtered, 'All data (with or without task tags)': df_unfiltered}

######################## Part 2a: Function to get user choice on filtered/unfiltered df ########################

# Function that returns filtered or unfiltered df
def user_df_choice(user_choice=str):
    return df_dict[user_choice]

######################## Part 2b: Call user_df_choice function to get filtered/unfiltered df ########################

# TODO Turn this into a user input
user_df = user_df_choice('Data with task tags only')
# Reindex the user_df
user_df = user_df.reset_index(drop=True)

######################## Part 2: Functions for data sub-sets and queries needed for visualizations ########################

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

# Get the project and task column based multi-index df
project_multi_df = create_multi_index_df(user_df, ['Project', 'Task'])
task_multi_df = create_multi_index_df(user_df, ['Task', 'Project'])

# Get project and task grouped absolute sum dfs
project_sum_df = sum_df_on_mi(project_multi_df, ['Project'], ['Time (h)'])
task_sum_df = sum_df_on_mi(task_multi_df, ['Task'], ['Time (h)'])

# Get project and task grouped second level sum dfs
project_task_sum_df = sum_df_on_mi(project_multi_df, ['Project', 'Task'], ['Time (h)'])
task_project_sum_df = sum_df_on_mi(task_multi_df, ['Task', 'Project'], ['Time (h)'])


######################## Part 4: Viz  ########################
app = dash.Dash()

app.layout = html.Div([

    html.Div([

######################## Part 4A: Header ########################
dcc.Markdown('''
# Component Design Productivity Calculator
*Based on Clockify time entries and actual production data*

***


### Inputs
'''),
]),
######################## Part 4B: Inputs ########################

# Left div for all the inputs
html.Div([
    # Task dropdown
    html.Div([
        html.Label('Task tag'),
        dcc.Dropdown(
            id='task-input',
            options=[{'label': i, 'value': i} for i in sorted(list(user_df['Task'].unique()))],
            value=''
            ),
        ],
        style={'margin-top': '25px'},
        ),

    # Date range dropdown
    html.Div([
        html.Label('Export data date range'),
        dcc.DatePickerRange(
            id='date-range',
            min_date_allowed=min(user_df['Start Date']),
            max_date_allowed=max(user_df['End Date']),
            initial_visible_month=dt.date.today(),
            start_date=dt.date.today() - dt.timedelta(days=60),
            end_date=dt.date.today()
            ),
        ],
        style={'margin-top': '25px'}),

    # Production div
    html.Div([
        html.Label('Production for this task-project-duration mix'),
        html.Div([
            # Left div for input field
            html.Div([
                dcc.Input(
                    id='production',
                    type='text'),
                ],
                style={'width': '46%', 'display': 'inline-block'}),
            # Right div for input unit
            html.Div(
                id='production-unit',
                style={'width': '20%', 'display': 'inline-block', 'text-align': 'left'}
                )
            ],
            ),


    # Project dropdown
    html.Div([
        html.Label('Project tag(s)'),
        dcc.Dropdown(
            id='project-input',
            options=[{'label': i, 'value': i} for i in sorted(list(user_df['Project'].unique()))],
            value='',
            multi=True
            ),
        ],
        style={'margin-top': '25px'},
        ),

    # Data type dropdown
    html.Div([
        html.Label('Export data type'),
        dcc.Dropdown(
            id='data-input',
            options=[{'label': i, 'value': i} for i in sorted(list(df_dict.keys()))],
            value='All data'
            ),
        ],
        style={'margin-top': '25px'},
        ),

        # Compute button div
        html.Div([
            html.Label('Calculate productivity for this task-project-duration mix'),
            html.Button('Run', id='button'),
            ],
            style={'margin-top': '25px'}),

        ],
        style={'margin-top': '25px'}
        ),

    ],
    # Overall left div set to 30% of screen
    style={'width': '30%',}
    ),

html.Hr(),            
])

######################## Part 4: Callbacks and functions ########################

@app.callback(
    Output(component_id='production-unit', component_property='children'),
    [Input(component_id='task-input', component_property='value')]
    )
def update_production_unit(input_value):
    return UNITS[input_value]


######################## Part 5: Run the app ########################

app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})

if __name__ == '__main__':
    app.run_server()
