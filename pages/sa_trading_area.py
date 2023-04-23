import streamlit as st

st.title("Trading Area Analysis")

# st.write(st.session_state.omc_sales)

options_month = st.session_state.omc_sales['Month'].unique()
options_fy = st.session_state.omc_sales['FiscalYear'].unique()[1:]
options_ta = st.session_state.omc_master['Trading Area'].unique()

col1, col2 = st.columns(2)
with col1:
    chosen_month = st.multiselect(label="Choose Month", options=options_month)

with col2:
    chosen_fy = st.multiselect(label="Choose Fiscal Year", options=options_fy)
chosen_ta = st.multiselect(label="Trading Area", options=options_ta)