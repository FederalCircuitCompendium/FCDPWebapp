# -*- coding: utf-8 -*-
"""
Created on Thu Feb 16 20:00:30 2023

@author: samda
"""

import pandas as pd
import streamlit as st
from config import document_data_link, document_codebook_link, dtype_dict, filter_dataframe, load_data, cafc_website

# set screen display to wide
st.set_page_config(layout="wide")

# create sections on page
header = st.container()
data_section = st.container()

## header section
with header:
    st.title('The Federal Circuit Database Project')
    # link to code book
    st.write("""The Federal Circuit Database Project a a database created to provide a central repository for
                researchers of the United States Court of Appeals for the Federal Circuit.
                The Compendium includes all opinions, orders, and summary affirmances that were
                released on the Federal Circuit’s website—essentially all opinions since 2004 and 
                all summary affirmances since 2007, along with numerous orders and other documents. 
                Additional documents have been added from collections conducted on PACER. Fields are coded in a 
                standardized format to allow future researchers to avoid recollecting fundamental fields such as 
                case names or opinion dates. The database also has the capacity for expansion, and new information about the decisions can 
                easily be added.  Public access to the database is provided via this web-based 
                interface, which allows for immediate visualization of data. In addition, copies of the individual
                datasets are archived at https://dataverse.harvard.edu/dataverse/CAFC_Dataset_Project""")
    
    st.write("""Access the document and docket datasets by using the links to the left.""")
    
    st.write("""Note that the Federal Circuit Dataset Project is not affiliated with the United States Court of 
                Appeals for the Federal Circuit. The court's website may be accessed at""",
                "[https://cafc.uscourts.gov.](%s)" % cafc_website)
    

    
