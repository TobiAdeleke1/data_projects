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
