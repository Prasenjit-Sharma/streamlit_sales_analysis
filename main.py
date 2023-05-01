import pandas as pd
from read_data import ReadData
from data_analysis import DataAnalysis
import streamlit as st
from streamlit_option_menu import option_menu
from streamlit_extras.switch_page_button import switch_page


# Read Data
@st.cache_data
def read_database():
    d = ReadData()
    return d


# Create the initial dataframes
data = read_database()
omc_master = data.omc_master
omc_sales = data.omc_sales
print(omc_master.columns)
st.session_state.omc_master=data.omc_master
st.session_state.omc_sales=data.omc_sales

# Horizontal Option Menu
selected = option_menu(None, ["Home", "Upload", "Tasks", 'Settings'],
                       icons=['house', 'cloud-upload', "list-task", 'gear'],
                       menu_icon="cast", default_index=0, orientation="horizontal")
selected


product = ["MS"]
SA = ['JODHPUR A']
OMC = ['HPC', 'BPC', 'IOC']

options_month = omc_sales['Month'].unique()
options_fy = omc_sales['FiscalYear'].unique()[1:]

st.title("Market Share")
chosen_month = st.multiselect(label="Choose Month", options=options_month)
chosen_fy = st.multiselect(label="Choose Fiscal Year", options=options_fy)
curr_fy = chosen_fy

filtered_omc_master = DataAnalysis.filter_data(df=omc_master, OMC=OMC, SA=SA)
curr_omc_sales = DataAnalysis.filter_data(df=omc_sales, Month=chosen_month, FiscalYear=curr_fy, PRODUCT=product)
hist_fy = DataAnalysis.return_hist_fy(curr_fy)
hist_omc_sales = DataAnalysis.filter_data(df=omc_sales, Month=chosen_month, FiscalYear=hist_fy, PRODUCT=product)

mkt_sh = DataAnalysis.omc_mkt_sh_dataframe(curr_omc_sales=curr_omc_sales,
                                           hist_omc_sales=hist_omc_sales,
                                           filtered_omc_master=filtered_omc_master)
# print(mkt_sh.head())

st.table(mkt_sh)
st.bar_chart(data=mkt_sh, y='Mkt Sh Diff')
