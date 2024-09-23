
import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# Create a connection object.
conn = st.connection("gsheets", type=GSheetsConnection)

# Lê os dados existentes
df = conn.read(
    worksheet="Folha",
    ttl="0m",
    usecols=[0, 1],
)

# Exibe os dados existentes
st.write("Dados existentes:")
st.dataframe(df)

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

# Lê os dados atualizados
updated_df = conn.read(
    worksheet="Folha",
    ttl="0",  # Define ttl para 0 para forçar uma nova leitura
    usecols=[0, 1],
)

# Exibe os dados atualizados
st.write("Dados atualizados:")
st.dataframe(updated_df)

# Print results.
for row in updated_df.itertuples():
    st.write(f"{row.Name} has a :{row.Button}:")