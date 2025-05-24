import streamlit as st
from database import DB
from widgets import Widgets
from typing import Literal, cast
import os


#inits
widgets = Widgets()

# initialize database coonections
db1 = DB()

with st.container(border=True):
    img, hero = st.columns([.25,.75])
    with img:
        st.image(os.path.join('btkt.png'))
    with hero:
        st.title('BoToKoTo BTKT')
        st.caption('A simple Data Viewer for 2025 Midterm Election Data for Partylist and Senators.')

widgets.rankings(cast(Literal['Partylist', 'Senators'],'Senators'))
widgets.rankings(cast(Literal['Partylist', 'Senators'], 'Partylist'))

with st.container(border=True):
    st.subheader('Set Lookup', divider=True)
    #sections
    acol1, acol2 = st.columns([1,1])
    bcol1, bcol2 = st.columns([1,1])

    with st.form('search-query'):
        with acol1:
            showTable = st.selectbox('Table', ["Senators","Partylist"])
        with acol2:

            # manage table headers

            #params
            fetch_table = "senator_votes" if showTable == "Senators" else "partylist_votes"
            starting_index = 12 if showTable == 'Partylist' else 13

            #create columnList
            fixed_cols = [" ".join(x[1].split(" ")[1:]) for x in db1.get_cols(cast(Literal['Partylist', 'Senators'], showTable))][starting_index:]
            raw_cols = [str(x[1]) for x in db1.get_cols(cast(Literal['Partylist', 'Senators'], showTable))][starting_index:]

            #apply to lookUp
            lookup = st.selectbox(showTable, fixed_cols)


        st.write('__:orange[Location Field Settings]__')

        unique_muni = db1.query(f'SELECT DISTINCT municipality, province  FROM {fetch_table}')
        muni = st.selectbox('City/Municipality', [f"{x[0]} ({x[1].title()})" for x in unique_muni], key='selection-bycitymuni')

        unique_barangay = db1.query(f'SELECT DISTINCT barangay, municipality, province  FROM {fetch_table}')
        brgy = st.selectbox('Barangay', [f"{x[0]} ({x[1].title()}, {x[2].title()})"  for x in unique_barangay],  key='selection-bybrgy')
        
        #filter settings
        enable_byMuni = st.checkbox("Show by City/Municipality Level")
        enable_byBarangay = st.checkbox("Show by Barangay Level")

        run = st.form_submit_button("Run")
        
    if run:
        widgets.showVotes(votes=db1.query(f'SELECT SUM("{raw_cols[fixed_cols.index(lookup)]}") FROM {fetch_table}')[0][0], candidate=lookup)
        widgets.showVotes_byRegion(dataSet=db1.query(f'SELECT SUM("{raw_cols[fixed_cols.index(lookup)]}") as votes,region FROM {fetch_table} GROUP BY region ORDER BY votes DESC'), candidate=lookup )
        widgets.showVotes_byProvince(dataSet=db1.query(f'SELECT SUM("{raw_cols[fixed_cols.index(lookup)]}") as votes,province FROM {fetch_table} GROUP BY province ORDER BY votes DESC'), candidate=lookup )
        if enable_byMuni:
            widgets.showVotes_by_specificCity(muni, candidate=raw_cols[fixed_cols.index(lookup)], table=fetch_table)
        if enable_byBarangay:
            widgets.showVotes_by_specificBrgy(brgy, candidate=raw_cols[fixed_cols.index(lookup)], table=fetch_table)
        # with st.container(border=True):
        #     widgets.rankings(cast(Literal['Senators', 'Partylist'], showTable))

