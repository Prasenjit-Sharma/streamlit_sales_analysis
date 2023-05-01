import streamlit as st
from data_analysis import DataAnalysis
import plotly.express as px
import plotly.figure_factory as ff

st.title("SA Market Share Analysis")

options_month = st.session_state.omc_sales['Month'].unique()
options_fy = st.session_state.omc_sales['FiscalYear'].unique()[1:]
options_product = st.session_state.omc_sales['PRODUCT'].unique()
options_OMC = st.session_state.omc_master['OMC'].unique()
options_sa = st.session_state.omc_master['SA'].unique()

col1, col2 = st.columns(2)
with col1:
    chosen_month = st.multiselect(label="Choose Month", options=options_month)

with col2:
    chosen_fy = st.multiselect(label="Choose Fiscal Year", options=options_fy)

chosen_product = st.multiselect(label="PRODUCT", options=options_product)
curr_fy = chosen_fy

filtered_omc_master = DataAnalysis.filter_data(df=st.session_state.omc_master, OMC=options_OMC)
curr_omc_sales = DataAnalysis.filter_data(df=st.session_state.omc_sales, Month=chosen_month, FiscalYear=curr_fy,
                                          PRODUCT=chosen_product)
hist_fy = DataAnalysis.return_hist_fy(curr_fy)
hist_omc_sales = DataAnalysis.filter_data(df=st.session_state.omc_sales, Month=chosen_month, FiscalYear=hist_fy,
                                          PRODUCT=chosen_product)

mkt_sh = DataAnalysis.omc_mkt_sh_dataframe(curr_omc_sales=curr_omc_sales,
                                           hist_omc_sales=hist_omc_sales,
                                           filtered_omc_master=filtered_omc_master)
# print(mkt_sh.head())
mkt_sh = mkt_sh.reset_index()

# st.table(mkt_sh)
# st.bar_chart(data=mkt_sh, y='Mkt Sh Diff')

fig = ff.create_table(mkt_sh)
st.plotly_chart(fig, use_container_width=True)

fig = px.bar(data_frame=mkt_sh, x='OMC', y='Mkt Sh Diff', text_auto=True, color='OMC',
             color_discrete_map={
                 "HPC": "blue",
                 "BPC": "yellow",
                 "IOC": "red"})
st.plotly_chart(fig, use_container_width=True)
