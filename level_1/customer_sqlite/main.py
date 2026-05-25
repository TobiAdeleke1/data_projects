import os
import streamlit as st
import pandas as pd 
from db import BASE_DIR, QueryDB

#1. Get a list of the queries to execute against db
QUERY_DICT = {
    sql_file.split('.')[0] : sql_file 
    for sql_file in os.listdir(os.path.join(BASE_DIR, 'queries'))
    if sql_file.endswith('.sql')
    }

# 2. Get db executor
qdb = QueryDB()
curr = qdb.get_cursor()
result_dict = {}
for query in QUERY_DICT:
    statement = qdb.get_sql_statement(QUERY_DICT[query])
    query_result = qdb.execute_query(statement)
    result_dict[query] = query_result

qdb.close_connection()

df_revenue = pd.DataFrame(
    result_dict['revenue_total_order'],
    columns=["status","revenue", "total_orders"],
)

df_customer_spend = pd.DataFrame(
    result_dict['above_average_customer_spend'], 
    columns=["customers","total_spend" ]
)
df_shipped_orders = pd.DataFrame(
    result_dict['top_regions_shipped_orders'], 
    columns=["region","total_spend" ],
)
df_spending_customers = pd.DataFrame(
    result_dict['top_spending_customers'], 
    columns=["region","tier","total_spend"]
)

# #3. Streamlit Dashboard
col1, col2= st.columns(2)
col3, col4 = st.columns(2, vertical_alignment="bottom")

with col1:
    st.subheader("Revenue and order count by status.")
    st.table(df_revenue, hide_index=True)

with col2:
    st.subheader("Customers with above average shipped spend.")
    st.table(df_customer_spend, hide_index=True)

with col3:
    st.subheader("Top 3 regions by shipped revenue.")
    st.table(df_shipped_orders, hide_index=True)

with col4:
    st.subheader("Total spend per customer for shipped orders.")
    st.table(df_spending_customers, hide_index=True)

