import streamlit as st
from database import DB

with st.expander('Advanced', expanded=False):
    with st.form('SQLite3-QueryMaster'):
        query = st.text_area('SQLite Query', height=100, placeholder='SELECT * FROM table')
        run = st.form_submit_button('Run Query')
        if run:
            db = DB()
            st.divider()
            st.caption('Running Query')
            st.code(query,"sql")
            st.caption('Response')
            st.write(db.query(query))