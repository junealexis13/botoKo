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


    def rankings(self, mode: Literal['Senators','Partylist']):
        match mode:
            case 'Senators':
                query_STR = "\n"
                for x in self.get_cols("Senators")[12:]:
                    query_STR+=f'SUM("{x[1]}"), \n'
                fixed_cols = [" ".join(x[1].split(" ")[1:]) for x in self.get_cols("Senators")][12:]
                resp = self.query(f'SELECT {query_STR[:-3]} FROM senator_votes')

                #cast to df
                df = pd.DataFrame(data=resp,columns=fixed_cols).T
                df.columns = ['votes']
                sorted = df.sort_values(by='votes', ascending=False)

                st.subheader('Senatorial Rankings - Midterm Election 2025',divider=True)
                fig = go.Figure()
                fig.add_trace(go.Bar(x=sorted.index,y=sorted['votes'][:15], showlegend=False))
                fig.update_traces(marker_color=['#17e6a4']*12 + ['#ed5e45']*3)
                fig.add_trace(go.Bar(
                            x=[None],
                            y=[None],
                            name='Green Bars (Magic 12)',
                            marker_color='#17e6a4'
                        ))

                fig.add_trace(go.Bar(
                            x=[None],
                            y=[None],
                            name='Red Bars (Didn"t made it)',
                            marker_color='#ed5e45'
                        ))
                st.plotly_chart(fig, use_container_width=True, theme='streamlit')

    def showVotes(self, votes: int, candidate: str):
        path_dir: str = os.path.join('templates','showvotes.html')
        f = open(path_dir,'r', encoding='utf-8')
        html = f.read().format(candidate,f"{votes:,}")
        st.html(html.format(votes, candidate))
    
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

    def showVotes_byProvince(self, dataSet: list, candidate: str):
        with st.container(border=True):
            st.subheader('Provincial Vote Summary', divider=True)
            dataSet = [x[::-1] for x in dataSet]
            df = pd.DataFrame(data=dataSet[:20], columns=['Province','Votes'])
            fig = px.bar(df.sort_values(by='Votes', ascending=False), 
                        x='Province', 
                        y='Votes', 
                        color='Votes',
                        color_continuous_scale='RdPu_r',
                        text='Votes')
            
            fig.update_layout(
                title=f'TOP20 Provinces who voted for {candidate}',  
                title_font_size=16, 
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

    def showVotes_by_specificCity(self, city_address:str, candidate:str, table: str):
        with st.container(border=True):
            st.subheader('Specified Location (City/Municipality)', divider=True)

            citymuni, province = city_address.split(" (")
            dataset = self.query(f'''SELECT SUM("{candidate}")
                                 FROM {table} 
                                 WHERE municipality = "{citymuni}"
                                    AND province = "{province.upper().strip(")")}"''')
            st.write(dataset)