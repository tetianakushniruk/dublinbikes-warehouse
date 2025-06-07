import streamlit as st
import duckdb
import pandas as pd

st.set_page_config(page_title="Dublin Bikes Live", page_icon=":bike:", layout="wide")
conn = duckdb.connect("warehouse.duckdb")
query = """
    SELECT * FROM fact_bike_availability
    ORDER BY recorded_at_minute DESC
    LIMIT 1000
"""
result = conn.execute(query)
df = result.fetch_df()
st.title("Dublin Bikes Availability")
st.write(f"Found {len(df)} rows of data")
st.dataframe(df)