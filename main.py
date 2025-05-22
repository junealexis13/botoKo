import streamlit as st
from database import DB

with st.container(border=True):
    st.title('BoToKoTo')
    st.caption('A simple Geographical Viewer for 2025 Midterm Election Data for Partylist and Senators.')

with st.container(border=True):
    st.subheader('Choose scope', divider=True)
    scope = st.selectbox('Level',['National Level','Provincial Level','City/Municipal Level','Barangay Level'])

    #<-- code logic here-->

with st.form('SQLite3-QueryMaster'):
    query = st.text_area('SQLite Query', height=350, placeholder='SELECT * FROM table')
    run = st.form_submit_button('Run Query')
    if run:
        db = DB()
        st.divider()
        st.caption('Running Query')
        st.code(query,"sql")
        st.caption('Response')
        st.write(db.query(query))