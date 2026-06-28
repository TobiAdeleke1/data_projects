import os
import streamlit as st
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()
BASE_DIR = os.path.dirname(os.path.abspath(__name__))
QUERY_PATH = os.path.join(BASE_DIR, 'queries' )
query_dict = {
    name.split('.')[0] : os.path.join(QUERY_PATH, name) 
    for name in os.listdir(QUERY_PATH) if name.endswith('.sql')
    }

engine = create_engine(
    f"postgresql://{os.environ["DB_USER"]}:{os.environ["DB_PASS"]}"
    f"@{os.environ["DB_HOST"]}:{os.environ["DB_PORT"]}/{os.environ["DB_NAME"]}"
)

with engine.connect() as conn:
    for f_name in query_dict:
        f_path = query_dict[f_name]
        with open(f_path) as sql_file: 
            query_data = sql_file.read()
            db_result = pd.read_sql(text(query_data), con=conn)
            query_dict[f_name] = db_result

# Streamlit Display
st.subheader("SEC: Companies Quarterly Analytics.")
st.dataframe(
    query_dict['quarterly'],
    hide_index=True)

st.subheader("SEC: Companies Yearly Analytics.")
st.dataframe(
        query_dict['yearly'],
        hide_index=True)