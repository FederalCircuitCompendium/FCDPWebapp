# -*- coding: utf-8 -*-
"""
Created on Wed Jul 05 12:52:47 2023

@author: jarantanen
"""

import pandas as pd
import streamlit as st
from config import document_data_link, document_codebook_link, dtype_dict, filter_dataframe, load_data

pd.set_option("styler.render.max_elements", 100_999_999)

# set screen display to wide
st.set_page_config(layout="wide")

# create sections on page
header = st.container()
data_section = st.container()

## header section
with header:
    st.title('Federal Circuit Document Dataset')
    st.write("[The current codebook for the document dataset may be downloaded here.](%s)" % document_codebook_link)



## data section
with data_section: 
   
    # read in data and display
    df = load_data(document_data_link, 
                   state_name = 'df', dtype_dict = dtype_dict)
         
    # set up columns for widgets
    col1, col2 = st.columns(2)
    
    # option to select columns to exclude from dataframe
    with col1:
        select_cols = st.checkbox("Click Here to Select Variables")
        if select_cols:
            df_cols = st.multiselect("Select Columns:", df.columns)
            # include selected columns
            df_cols = [col for col in df.columns if col in df_cols]
            # return dataframe with selected columns
            df = df[df_cols]
    
    # convert data to streamlit DataFrame with filtering options
    with col2:
        df_filtered = filter_dataframe(df)
        
    # Display the filtered dataframe 
    st.dataframe(df_filtered, use_container_width = True) 
        
    # create a dataframe with no commas in the year. However, it makes the dataset load much slower. head(1000) is used to mitigate this.    
    ## st.dataframe(df_filtered.head(1000).style.format(thousands="", subset="docYear"), use_container_width = True)
    
    # function to convert data to csv
    def convert_df(df):
        return df.to_csv(index = False).encode('utf-8')
    
    # convert filtered data to csv
    csv = convert_df(df_filtered)
    
    # download option
    st.download_button(label = 'Download Dataset', 
                       data = csv,
                       file_name = 'federal_circuit_decisions_dataset.csv',
                       mime = 'text/csv')
    st.write('Note: Download will reflect any filtering performed on the data')