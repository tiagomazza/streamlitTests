
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
    usecols=[0, 1],
    nrows=30,
)

# Remove linhas completamente vazias
df = df.dropna(how='all').reset_index(drop=True)

# Cria um formulário para adicionar novos dados
with st.form("add_data"):
    new_name = st.text_input("Nome")
    new_button = st.text_input("Botão")
    submitted = st.form_submit_button("Adicionar")

    if submitted:
        # Encontra o primeiro índice vazio
        first_empty_index = df.index[df.isnull().all(axis=1)].min()
        
        if pd.isna(first_empty_index):
            # Se não houver linhas vazias, adiciona ao final
            first_empty_index = len(df)
        
        # Cria um novo DataFrame com os dados do formulário
        new_data = pd.DataFrame({"Name": [new_name], "Button": [new_button]})
        
        # Insere os novos dados na primeira linha vazia
        df.loc[first_empty_index] = new_data.iloc[0]
        
        # Atualiza a planilha
        conn.update(data=df, worksheet="Folha")
        
        st.success("Dados adicionados com sucesso!")

# Lê os dados atualizados
updated_df = conn.read(
    worksheet="Folha",
    ttl="0",  # Define ttl para 0 para forçar uma nova leitura
    usecols=[0, 1],
    nrows=30,
)


