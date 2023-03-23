# -*- coding: utf-8 -*-
"""
Created on Wed Mar 22 21:21:47 2023

@author: samda
"""

import pandas as pd
import streamlit as st
from pandas.api.types import (
    is_categorical_dtype,
    is_datetime64_any_dtype,
    is_numeric_dtype,
    is_object_dtype,
)

# create sections on page
header = st.container()
data_section = st.container()

# function to filter data
# see blog: https://blog.streamlit.io/auto-generate-a-dataframe-filtering-ui-in-streamlit-with-filter_dataframe/
def filter_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Adds a UI on top of a dataframe to let viewers filter columns

    Args:
        df (pd.DataFrame): Original dataframe

    Returns:
        pd.DataFrame: Filtered dataframe
    """
    modify = st.checkbox("Filter Data")

    if not modify:
        return df

    df = df.copy()

    # Try to convert datetimes into a standard format (datetime, no timezone)
    for col in df.columns:
        if is_object_dtype(df[col]):
            try:
                df[col] = pd.to_datetime(df[col])
            except Exception:
                pass

        # local time zone conversion
        if is_datetime64_any_dtype(df[col]):
            df[col] = df[col].dt.tz_localize(None)

    modification_container = st.container()

    with modification_container:
        to_filter_columns = st.multiselect("Filter dataframe on", df.columns)
        for column in to_filter_columns:
            left, right = st.columns((1, 20))
            
            # Select categories for categorical data type
            # Treat columns with < 10 unique values as categorical
            if is_categorical_dtype(df[column]) or df[column].nunique() < 10:
                user_cat_input = right.multiselect(
                    f"Values for {column}",
                    df[column].unique(),
                    default=list(df[column].unique()),
                )
                df = df[df[column].isin(user_cat_input)]
                
            # slider for numeric data type
            elif is_numeric_dtype(df[column]):
                _min = float(df[column].min())
                _max = float(df[column].max())
                step = (_max - _min) / 100
                user_num_input = right.slider(
                    f"Values for {column}",
                    min_value=_min,
                    max_value=_max,
                    value=(_min, _max),
                    step=step,
                )
                df = df[df[column].between(*user_num_input)]
                
            # date range for datetime64 data type
            elif is_datetime64_any_dtype(df[column]):
                user_date_input = right.date_input(
                    f"Values for {column}",
                    value=(
                        df[column].min(),
                        df[column].max(),
                    ),
                )
                if len(user_date_input) == 2:
                    user_date_input = tuple(map(pd.to_datetime, user_date_input))
                    start_date, end_date = user_date_input
                    df = df.loc[df[column].between(start_date, end_date)]
                    
            # treat everything else like a string
            # search function for strings
            else:
                user_text_input = right.text_input(
                    f"Substring or regex in {column}",
                )
                if user_text_input:
                    df = df[df[column].astype(str).str.contains(user_text_input, case = False)]

    return df

## header section
with header:
    st.title('Federal Circuit Docket Dataset')
    
## data section
with data_section:
    
    # define function to load data
    # st.cache_data means the data is stored and doesn't need to be read again each time the user changes a variable
    @st.cache_data
    def load_data(data_path, state_name):
        '''
        Parameters
        ----------
        data_path : str
            The file path to load the data
        state_name : str
            The name that the DataFrame will be stored as in the session state

        Returns
        -------
        df : DataFrame
        '''
        df = pd.read_csv(data_path, sep = '\t')
        # save the data in the session_state so it can be accessed from other pages
        st.session_state[state_name] = df
        return df
    
    # read in data and display
    df_dock = load_data('https://raw.githubusercontent.com/sdannels/Federal_Circuit_Decisions_Beta/main/Data/2022-12-31%20CAFC%20Dockets.tab', state_name = 'df_dock')
    
    # set up columns for widgets
    col1, col2 = st.columns(2)
    
    # option to select columns to exclude from dataframe
    with col1:
        select_cols = st.checkbox("Select Variables")
        if select_cols:
            df_dock_cols = st.multiselect("Select Columns:", df_dock.columns)
            # include selected columns
            df_dock_cols = [col for col in df_dock.columns if col in df_dock_cols]
            # return dataframe with selected columns
            df_dock = df_dock[df_dock_cols]
    
    # convert data to streamlit DataFrame with filtering options
    with col2:
        df_dock_filtered = filter_dataframe(df_dock)
    st.dataframe(df_dock_filtered, use_container_width = True)
    
    # function to convert data to csv
    def convert_df(df):
        return df.to_csv(index = False).encode('utf-8')
    
    # convert filtered data to csv
    csv_dock = convert_df(df_dock_filtered)
    
    # download option
    st.download_button(label = 'Download Dataset', 
                       data = csv_dock,
                       file_name = 'federal_circuit_docket_dataset.csv',
                       mime = 'text/csv')
    st.write('Note: Download will reflect any filtering performed on the data')