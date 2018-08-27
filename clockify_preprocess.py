# -*- coding: utf-8 -*-
"""
Created on Tue Aug 21 11:39:09 2018

@author: Afaan.Naqvi
"""
import pandas as pd
import numpy as np
import os
from functools import reduce

################# CONSTANTS #################
ROOT_DIR = '../RawExportData/'

################# READ + CLEAN USER SELECTED FILES  #################
# Function to parse out the start week date out of a file name
def get_start_date(file=str):
    # Split file name on 'clockify-report-' and take the first element of the second element split on '-to-'
    start_date = file.split('clockify_report_')[1].split('_to')[0]
    return start_date

def get_end_date(file=str):
    # Split file name on 'to_' and take the second element
    end_date = file.split('to_')[1].split('.xlsx')[0]
    return end_date

# Function to read and prep a df
def read_prep_df(data_file, parent_folder):
    file_df = pd.read_excel(data_file, skiprows=1)
    # Fill the newline characters and white space with np.nan so they can be dropna later
    file_df.replace(to_replace=['\n', ''], value=np.nan, inplace=True)
    # Add the week start date to a new column (helpful later when multiple dfs are concatenated)
    file_df['Start Date'] = get_start_date(data_file)
    # Add the week end date to a new column (helpful later when multiple dfs are concatenated)
    file_df['End Date'] = get_end_date(data_file)
    # Add the task tag to a new column (from folder name)
    file_df['Task'] = str(parent_folder)
    # Fill the Nans in the project column only with a forward project fill (pad)
    file_df['Project'].fillna(method='pad', inplace=True)
    # Strip out the '\n' characters at the start of the project strings
    file_df['Project'] = file_df['Project'].apply(lambda x: x[1:])
    # Drop columns not needed
    file_df.drop(columns=['Hourly rate USD', 'Time (decimal)', 'Amount USD'], inplace=True)
    # Drop the total time rows in the df which are now Nan values in the 'Time Entry' column
    file_df.dropna(subset=['Time Entry'], how='all', inplace=True)
    # Set Time (h) column to time delta
    file_df['Time (h)'] = pd.to_timedelta(file_df['Time (h)'])
    # Set week start date column to datetime
    file_df['Start Date'] = pd.to_datetime(file_df['Start Date'])
    # Set week end date column to datetime
    file_df['End Date'] = pd.to_datetime(file_df['End Date'])
    return file_df

# Function to walk the data set folder to read and concatenate dfs
def read_and_concat_dfs(abs_path):
    df_list = []
    for roots, dirs, files in os.walk(ROOT_DIR):
        # Get the parent folder (task) name
        for direc in dirs:
            for roots, dirs, files in os.walk(ROOT_DIR + direc):
                # For each file in the parent folder
                for file in files:
                    df_list.append(read_prep_df(ROOT_DIR + direc + '/' + file, direc))
    data_df = pd.concat(df_list, ignore_index=True)
    return data_df

################# MAIN FUNCTION  #################
def main():
    # Read, clean, prep, and concat all the files int the user selected folder
    combined_df = read_and_concat_dfs(ROOT_DIR)

    return combined_df

################# CALL MAIN FUNCTION AND EXPORT TO CSV #################
consolidated_data = main()

# export final df to csv
consolidated_data.to_csv('../ConsolidatedData/consolidated_clockify_data.csv')