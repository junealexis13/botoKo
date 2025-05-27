import streamlit as st
from database import DB

db = DB()
with st.expander('Advanced', expanded=False):
    with st.form('SQLite3-QueryMaster'):
        query = st.text_area('SQLite Query', height=100, placeholder='SELECT * FROM table')
        run = st.form_submit_button('Run Query')
        if run:

            st.divider()
            st.caption('Running Query')
            st.code(query,"sql")
            st.caption('Response')
            st.write(db.query(query))

with st.expander('Set Querys', expanded=False):
    with st.form('SQLite3-QueryMaster-Set-Query'):
        bt, select_table = st.columns([.3,.7])
        with select_table:
            table = st.selectbox('Select Table', options=['senator_votes','partylist_votes'])
            query = f'PRAGMA table_info({table})'
        with bt:
            st.caption('Proceed')
            run = st.form_submit_button('Get Table Info Settings')
        
        if run:
            st.divider()
            st.caption('Running Query')
            st.code(query,"sql")
            st.caption('Response')
            st.write(db.query(query))