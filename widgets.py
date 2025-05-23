import streamlit as st
from database import DB
from typing import Literal

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

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