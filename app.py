
import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# Create a connection object.
conn = st.connection("gsheets", type=GSheetsConnection)

# Lê os dados existentes
df = conn.read(
    worksheet="Folha",
    ttl="10m",
    usecols=[0, 1],
    nrows=3,
)

# Cria um formulário para adicionar novos dados
with st.form("add_data"):
    new_name = st.text_input("Nome")
    new_button = st.text_input("Botão")
    submitted = st.form_submit_button("Adicionar")

    if submitted:
        # Cria um novo DataFrame com os dados do formulário
        new_data = pd.DataFrame({"Name": [new_name], "Button": [new_button]})
        
        # Concatena os novos dados com os existentes
        updated_df = pd.concat([df, new_data], ignore_index=True)
        
        # Atualiza a planilha
        conn.update(data=updated_df, worksheet="Folha")
        
        st.success("Dados adicionados com sucesso!")

