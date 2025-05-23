import streamlit as st
from database import DB
from widgets import Widgets

with st.container(border=True):
    st.title('BoToKoTo')
    st.caption('A simple Geographical Viewer for 2025 Midterm Election Data for Partylist and Senators.')

with st.container(border=True):
    st.subheader('Choose scope', divider=True)

    col1, col2 = st.columns([1,1])
    with col1:
        scope = st.selectbox('Level',['National Level','Provincial Level','City/Municipal Level','Barangay Level'])
    with col2:
        showTable = st.selectbox('Table', ["Senators","Partylist"])


    fetch_table = "senator_votes" if showTable == "Senators" else "partylist_votes"
    starting_index = 12 if showTable == 'Partylist' else 13
    
    db1 = DB()
    # manage table headers
    fixed_cols = [" ".join(x[1].split(" ")[1:]) for x in db1.get_cols(showTable)][starting_index:]
    raw_cols = [str(x[1]) for x in db1.get_cols(showTable)][starting_index:]

    lookup = st.selectbox(showTable, fixed_cols)

    run = st.button("Run")
    if run:
        match scope:
            case "National Level":
                getdata = db1.query(f'SELECT SUM("{raw_cols[fixed_cols.index(lookup)]}") FROM {fetch_table}')
                st.write(getdata[0][0])

        with st.container(border=True):
            widgets = Widgets()
            widgets.rankings(showTable)

with st.expander('Advanced', expanded=False):
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