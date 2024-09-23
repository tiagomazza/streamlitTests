
import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import numpy as np

# Create a connection object.
conn = st.connection("gsheets", type=GSheetsConnection)

# Lê os dados existentes
df = conn.read(
    worksheet="Folha",
    ttl="0m",
    usecols=[0, 1]
)

df = df.dropna(how='all').reset_index(drop=True)

with st.form("add_data"):
    new_name = st.text_input("Nome")
    new_button = st.text_input("Botão")
    submitted = st.form_submit_button("Adicionar")

    if submitted:
        first_empty_index = df.index[df.isnull().all(axis=1)].min()
        
        if pd.isna(first_empty_index):
            first_empty_index = len(df)
        
        new_data = pd.DataFrame({"Name": [new_name], "Button": [new_button]})
        
        df.loc[first_empty_index] = new_data.iloc[0]
    
        conn.update(data=df, worksheet="Folha")
        
        st.success("Dados adicionados com sucesso!")



