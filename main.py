import pandas as pd
from read_data import ReadData
from data_analysis import DataAnalysis
import streamlit as st

data = ReadData()
omc_master = data.omc_master
omc_sales = data.omc_sales
# print(omc_master.columns)

curr_month = ["Mar"]
curr_fy = ['22-23']
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
