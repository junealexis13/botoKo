import streamlit as st
from database import DB
from typing import Literal

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

import os, glob

class Widgets(DB):
    def __init__(self):
        super().__init__()


    def init_session_state(self):
        if "TOP_SEN" not in st.session_state:
            st.session_state['TOP_SEN'] = 15

        if "TOP_PARTY" not in st.session_state:
            st.session_state['TOP_PARTY'] = 30

    def get_total_votes(self, mode: Literal['Senators','Partylist']):
        match mode:
            case 'Senators':
                resp = self.query('SELECT SUM(registeredVoters) FROM senator_votes')
                return resp[0][0]
            case 'Partylist':
                resp = self.query('SELECT SUM(registeredVoters) FROM partylist_votes')
                return resp[0][0]
    def get_senator_ranking(self, candidate: str, table: str):
        query_STR = "\n"
        if table == "senator_votes":
            for x in self.get_cols("Senators")[12:]:
                query_STR+=f'SUM("{x[1]}"), \n'
            fixed_cols = [" ".join(x[1].split(" ")[1:]) for x in self.get_cols("Senators")][12:]
        else:
            for x in self.get_cols("Partylist")[12:]:
                query_STR+=f'SUM("{x[1]}"), \n'
            fixed_cols = [" ".join(x[1].split(" ")[1:]) for x in self.get_cols("Partylist")][12:]

    
        resp = self.query(f'SELECT {query_STR[:-3]} FROM {table}')
        df = pd.DataFrame(data=resp,columns=fixed_cols).T
        df.columns = ['votes']
        sortedDf = df.sort_values(by='votes', ascending=False)
        sortedDf['Ranking'] = range(1, len(sortedDf)+1)
        return sortedDf.loc[sortedDf.index == candidate]['Ranking'].values[0]

    def rankings(self, mode: Literal['Senators','Partylist']):
        match mode:
            case 'Senators':
                with st.container(border=True):
                    st.subheader('Senatorial Rankings - Midterm Election 2025',divider=True)
                    cutoff = st.slider('Number of Candidates to Show', max_value=66,step=1, on_change=lambda: st.session_state.update({'TOP_SEN': cutoff}), value=st.session_state['TOP_SEN'])
                    if cutoff > 0:
                        query_STR = "\n"
                        for x in self.get_cols("Senators")[12:]:
                            query_STR+=f'SUM("{x[1]}"), \n'
                        fixed_cols = [" ".join(x[1].split(" ")[1:]) for x in self.get_cols("Senators")][12:]
                        resp = self.query(f'SELECT {query_STR[:-3]} FROM senator_votes')

                        #cast to df
                        df = pd.DataFrame(data=resp,columns=fixed_cols).T
                        df.columns = ['votes']
                        sorted = df.sort_values(by='votes', ascending=False)

                        fig = go.Figure()
                        fig.add_trace(go.Bar(x=sorted.index,y=sorted['votes'][:cutoff],  text=sorted['votes'][:cutoff]))

                        others = cutoff - 12
                        fig.update_traces(marker_color=['#17e6a4']*12 + ['#ed5e45']*others,
                                        texttemplate='%{text:,}',     
                                        textposition='inside')    
                        
                        fig.update_layout(
                            title=f'Showing Top {cutoff} candidates - Magic 12 in Green',
                            xaxis_title='Senator',
                            xaxis=dict(
                            tickfont=dict(
                                family='Sans-serif', 
                                size=8,
                                )
                            )
                        )
                        st.plotly_chart(fig, use_container_width=True, theme='streamlit')

            case 'Partylist':
                with st.container(border=True):
                    query_STR = "\n"
                    st.subheader('Partylist Rankings - Midterm Election 2025',divider=True)
                    cutoff = st.slider('Number of Candidates to Show', max_value=156,step=1, on_change=lambda: st.session_state.update({'TOP_PARTY': cutoff}), value=st.session_state['TOP_PARTY'])
                    if cutoff > 0:
                        for x in self.get_cols("Partylist")[12:]:
                            query_STR+=f'SUM("{x[1]}"), \n'
                        fixed_cols = [" ".join(x[1].split(" ")[1:]) for x in self.get_cols("Partylist")][12:]
                        resp = self.query(f'SELECT {query_STR[:-3]} FROM partylist_votes')

                        #cast to df
                        df = pd.DataFrame(data=resp,columns=fixed_cols).T
                        df.columns = ['votes']
                        sorted = df.sort_values(by='votes', ascending=False)


                        fig = go.Figure()
                        fig.add_trace(go.Bar(x=sorted.index,y=sorted['votes'][:cutoff],
                                            text=sorted['votes'][:cutoff],
                                            ))

                        fig.update_traces(marker_color="#d8e617",
                                        texttemplate='%{text:,}',     
                                        textposition='inside')    
                        
                        fig.update_layout(
                            title=f'Showing Top {cutoff} candidates',
                            xaxis_title='Partylist',
                            xaxis=dict(
                            tickfont=dict(
                                family='Sans-serif', 
                                size=8,
                                )
                            ),
                            legend=dict(
                                orientation="h", 
                                yanchor="top",            
                                xanchor="center",
                            )
                        )
                        st.plotly_chart(fig, use_container_width=True, theme='streamlit')

    def showVotes(self, votes: int, candidate: str, table: str):
        path_dir: str = os.path.join('templates','showvotes.html')
        f = open(path_dir,'r', encoding='utf-8')
        ranking = self.get_senator_ranking(candidate=candidate, table=table)
        html = f.read().format(candidate,f"{votes:,}", ranking)

        self.get_senator_ranking(candidate, table) if table == 'senator_votes' else None

        fig = go.Figure()
        fig.add_trace(go.Pie(labels= ['Voted for', "Didn't Voted"],
                                values = [votes, self.get_total_votes('Senators' if table == 'senator_votes' else 'Partylist') - votes],
                                textinfo='label+percent',
                                textfont_size=14,
                                textposition='inside',
                                pull=0.05,
                                marker=dict(colors=['#17e6a4','#ed5e45']),
                                hoverinfo='label+percent+value',
                                hole=.5
                                ))
        fig.update_layout(
            title=f'Votes for {candidate}',
            title_font_size=16,
            height=500,
            legend=dict(
                orientation="h", 
                yanchor="top",            
                xanchor="center",
                y=-0.2
            )
        )
        st.plotly_chart(fig, use_container_width=True, theme='streamlit')
        st.html(html.format(votes, candidate, ranking))
    
    def showVotes_byRegion(self, dataSet: list, candidate: str):
        with st.container(border=True):
            st.subheader('Regional Vote Summary', divider=True)
            dataSet = [x[::-1] for x in dataSet]
            df = pd.DataFrame(data=dataSet, columns=['Province','Votes'])
            fig = px.bar(df.sort_values(by='Votes', ascending=False), 
                        x='Province', 
                        y='Votes', 
                        color='Votes',
                        color_continuous_scale='Cividis',
                        text='Votes')
            
            fig.update_layout(
                title=f'Regional Votes for {candidate}',  
                title_font_size=16, 
                height=500,  
                yaxis_title='Votes',
                xaxis_title='Province',
                xaxis=dict(
                    tickfont=dict(
                        family='Sans-serif', 
                        size=8,
                        )
                    )
                )

            fig.update_traces(
                texttemplate='%{text:,}',     # format with comma
                textposition='outside',      # place label outside/above the bar
            )

            st.plotly_chart(fig, use_container_width=True, theme='streamlit')

    @st.fragment
    def showVotes_byProvince(self, dataSet: list, candidate: str):
        with st.container(border=True):
            st.subheader('Provincial Vote Summary', divider=True)
            dataSet = [x[::-1] for x in dataSet]
            df = pd.DataFrame(data=dataSet, columns=['Province','Votes'])

            cutoff = st.slider("Show No. of Provinces", max_value=len(df), value=int(len(df)/4))
            if cutoff > 0:
                fig = px.bar(df.sort_values(by='Votes', ascending=False)[:cutoff], 
                            x='Province', 
                            y='Votes', 
                            color='Votes',
                            color_continuous_scale='RdPu_r',
                            text='Votes')
                
                fig.update_layout(
                    title=f'Showing top {cutoff} Provinces that voted for {candidate}',  
                    title_font_size=14, 
                    yaxis_title='Votes',
                    xaxis_title='Province',
                    xaxis=dict(
                        tickfont=dict(
                            family='Sans-serif', 
                            size=6,
                            )
                        )
                    )

                fig.update_traces(
                    texttemplate='%{text:,}',     # format with comma
                    textposition='outside',      # place label outside/above the bar
                )

                st.plotly_chart(fig, use_container_width=True, theme='streamlit')

    @st.fragment
    def showVotes_by_specificCity(self, city_address:str, candidate:str, table: str):
        with st.container(border=True):
            st.subheader('Specified Location (City/Municipality or International)', divider=True)

            citymuni, province = city_address.split(" (")
            dataset = self.query(f'''SELECT SUM("{candidate}")
                                 FROM {table} 
                                 WHERE municipality = "{citymuni}"
                                    AND province = "{province.upper().strip(")")}"''')
            
            #create a component
            place = f'{citymuni}, {province.upper().strip(")")}'
            path_dir: str = os.path.join('templates','showvotes_city.html')
            f = open(path_dir,'r', encoding='utf-8')
            html = f.read().format(place,f"{dataset[0][0]:,}")
            st.html(html)



            perbrgy = self.query(f'''SELECT SUM("{candidate}"), barangay 
                                FROM {table} 
                                WHERE municipality="{citymuni}" GROUP BY barangay''')
            
            perbrgy = [x[::-1] for x in perbrgy]
            df = pd.DataFrame(data=perbrgy, columns=['Barangay','Votes'])

            cutoff = st.slider("Show No. of City", max_value=len(df), value=int(len(df)/4))
            if cutoff > 0:

                fig = px.bar(df.sort_values(by='Votes', ascending=False)[:cutoff], 
                            x='Barangay', 
                            y='Votes', 
                            color='Votes',
                            color_continuous_scale='Magma_r',
                            text='Votes')
                
                fig.update_layout(
                    title=f'Showing {cutoff} Brgys voted for {candidate}',  
                    title_font_size=16, 
                    yaxis_title='Votes',
                    xaxis_title='Barangay',
                    xaxis=dict(
                        tickfont=dict(
                            family='Sans-serif', 
                            size=8,
                            )
                        )
                    )

                fig.update_traces(
                    texttemplate='%{text:,}',     # format with comma
                    textposition='outside',      # place label outside/above the bar
                )

                st.plotly_chart(fig, use_container_width=True, theme='streamlit')

    def showVotes_by_specificBrgy(self, brgy_address:str, candidate:str, table: str):
        with st.container(border=True):
            st.subheader('Specified Location (Barangay Level)', divider=True)

            brgy, composite = brgy_address.split(" (")
            citymuni, province = composite.strip(")").split(", ")


            dataset = self.query(f'''SELECT SUM("{candidate}")
                                 FROM {table} 
                                 WHERE barangay = "{brgy}"
                                 AND municipality = "{citymuni.upper()}"
                                 AND province = "{province.upper()}"''')
            
            #create a component
            place = f'{brgy}, {citymuni}, {province.upper().strip(")")}'
            path_dir: str = os.path.join('templates','showvotes_brgy.html')
            f = open(path_dir,'r', encoding='utf-8')
            html = f.read().format(place,f"{dataset[0][0]:,}")
            st.html(html)