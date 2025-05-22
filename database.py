import sqlite3
import pandas as pd
import os, glob
from typing import Literal
import streamlit as st
import traceback

class DB:
    def __init__(self):
        self.con = sqlite3.connect('election_data.db')
        self.db = self.con.cursor()

    def table_exists(self, table_name: str) -> bool:
        self.db.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,)
        )
        return self.db.fetchone() is not None

    def create_table(self, table_name: str, dataframe: pd.DataFrame):
        if not self.table_exists(table_name):
            # Infer SQL column types from DataFrame
            cols_with_types = []
            for col in dataframe.columns:
                sample_val = dataframe[col].dropna().iloc[0] if not dataframe[col].dropna().empty else ""
                if isinstance(sample_val, int):
                    col_type = "INTEGER"
                elif isinstance(sample_val, float):
                    col_type = "REAL"
                else:
                    col_type = "TEXT"
                cols_with_types.append(f'"{col}" {col_type}')
            cols_str = ", ".join(cols_with_types)
            create_query = f"CREATE TABLE {table_name} ({cols_str})"
            self.db.execute(create_query)
            self.con.commit()

    def insert_data(self, values: tuple, table_name: str):
        placeholders = ','.join(['?'] * len(values))
        query = f"INSERT INTO {table_name} VALUES ({placeholders})"
        self.db.execute(query, values)

    def commit(self):
        self.con.commit()

    def query(self, query):
        try:
            response = self.con.execute(query)
            return response
        except Exception as e:
            err_msg = traceback.format_exc()
            st.error(f'Error: {e}')


class DataParse(DB):
    '''Mainly used to upload. Dataset are deprecated'''
    def __init__(self):
        self.datasets = glob.glob(os.path.join('datasets', '*'))

    def load_df(self, data: Literal['PL', "SEN"]):
        match data:
            case 'PL':
                return pd.read_csv(self.datasets[0])
            case 'SEN':
                return pd.read_csv(self.datasets[1])


if __name__ == "__main__":
    st.title('Database using SQLite 3')
    start = st.button('Start uploading')
    if start:

        a = DataParse()
        dataPL = a.load_df('PL')
        dataSEN = a.load_df('SEN')

        db = DB()
        db.create_table("partylist_votes", dataPL)
        db.create_table("senator_votes", dataSEN)

        # Insert Partylist data
        progress = st.progress(0, text='Processing PartyList Dataset')
        for i, (_, row) in enumerate(dataPL.iterrows()):
            db.insert_data(tuple(row), "partylist_votes")
            progress.progress((i + 1) / len(dataPL), text='Processing PartyList Dataset')
        db.commit()

        # Insert Senator data
        progress2 = st.progress(0, text='Processing Senator Dataset')
        for i, (_, row) in enumerate(dataSEN.iterrows()):
            db.insert_data(tuple(row), "senator_votes")
            progress2.progress((i + 1) / len(dataSEN), text='Processing Senator Dataset')
        db.commit()

        st.success("All data inserted successfully!")
