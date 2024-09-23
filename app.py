
import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

pagina_selecionada = st.sidebar.radio("", ["✍🏽Marcação de Ponto"])

def fill_missing_data(data_frame):
    default_entry_morning = pd.Timestamp.now().replace(hour=9, minute=0, second=0)
    default_exit_morning = pd.Timestamp.now().replace(hour=12, minute=30, second=0)
    default_entry_afternoon = pd.Timestamp.now().replace(hour=14, minute=30, second=0)
    default_exit_afternoon = pd.Timestamp.now().replace(hour=18, minute=0, second=0)
    
    for index, row in data_frame.iterrows():
        if pd.isnull(row['Entrada Manhã']):
            data_frame.at[index, 'Entrada Manhã'] = default_entry_morning

# Create a connection object.
conn = st.connection("gsheets", type=GSheetsConnection)

# Lê os dados existentes
df = conn.read(
    worksheet="Folha",
    ttl="0m",
    usecols=[0,1,2]
)

df = df.dropna(how='all').reset_index(drop=True)




# Adicionar campo de PIN
pin_digitado = st.text_input("Digite o seu PIN:")

# Verificar se o PIN foi digitado
# Determinar qual página exibir com base na seleção do usuário

if pagina_selecionada == "✍🏽Marcação de Ponto":
    st.title("✍🏽Marcação de Ponto")

    # Adicionar campo de PIN
    pin_digitado = st.text_input("Digite o seu PIN:")

    # Verificar se o PIN foi digitado
    if str(pin_digitado):
        # Ler os dados da aba "Dados" para encontrar o nome correspondente ao PIN inserido
        dados = conn.read(worksheet="Dados", usecols=["Pin", "Nome"], ttl=5)
               
        # Verificar se o PIN está na lista de PINs válidos
        try:
            pin_int = int(float(pin_digitado))
            if pin_int in dados["Pin"].tolist():
                nome = dados.loc[dados["Pin"] == pin_int, "Nome"].iloc[0]

            if st.button("☕ Entrada Manhã"):
                            # Obter a hora atual
                            current_time = datetime.now()
                            one_hour_after = current_time + timedelta(hours=1)
                            submission_datetime = one_hour_after.strftime("%Y-%m-%d %H:%M:%S")

                            # Criar nova linha com nome, botão e hora
                            new_data = pd.DataFrame({
                                "Name": [nome],
                                "Button": ["Entrada Manhã"],
                                "SubmissionDateTime": [submission_datetime]
                            })

                            # Carregar dados existentes
                            existing_data_reservations = conn.read(worksheet="Folha")
                            
                            # Remover linhas completamente vazias e resetar o índice
                            existing_data_reservations = existing_data_reservations.dropna(how='all').reset_index(drop=True)

                            # Encontrar o primeiro índice vazio
                            first_empty_index = existing_data_reservations.index[existing_data_reservations.isnull().all(axis=1)].min()
                            
                            if pd.isna(first_empty_index):
                                first_empty_index = len(existing_data_reservations)

                            # Adicionar nova linha no primeiro índice vazio
                            existing_data_reservations.loc[first_empty_index] = new_data.iloc[0]

                            # Atualizar a planilha com os novos dados
                            conn.update(worksheet="Folha", data=existing_data_reservations)

                            st.success("Dados registrados com sucesso!")


            if st.button("🌮 Saída Manhã"):
                            # Obter a hora atual
                            current_time = datetime.now()
                            one_hour_after = current_time + timedelta(hours=1)
                            submission_datetime = one_hour_after.strftime("%Y-%m-%d %H:%M:%S")

                            # Criar nova linha com nome, botão e hora
                            new_data = pd.DataFrame({
                                "Name": [nome],
                                "Button": ["Saída Manhã"],
                                "SubmissionDateTime": [submission_datetime]
                            })

                            # Carregar dados existentes
                            existing_data_reservations = conn.read(worksheet="Folha")
                            
                            # Remover linhas completamente vazias e resetar o índice
                            existing_data_reservations = existing_data_reservations.dropna(how='all').reset_index(drop=True)

                            # Encontrar o primeiro índice vazio
                            first_empty_index = existing_data_reservations.index[existing_data_reservations.isnull().all(axis=1)].min()
                            
                            if pd.isna(first_empty_index):
                                first_empty_index = len(existing_data_reservations)

                            # Adicionar nova linha no primeiro índice vazio
                            existing_data_reservations.loc[first_empty_index] = new_data.iloc[0]

                            # Atualizar a planilha com os novos dados
                            conn.update(worksheet="Folha", data=existing_data_reservations)

                            st.success("Dados registrados com sucesso!")

            if st.button("🌄 Entrada Tarde"):
                            # Obter a hora atual
                            current_time = datetime.now()
                            one_hour_after = current_time + timedelta(hours=1)
                            submission_datetime = one_hour_after.strftime("%Y-%m-%d %H:%M:%S")

                            # Criar nova linha com nome, botão e hora
                            new_data = pd.DataFrame({
                                "Name": [nome],
                                "Button": ["Entrada Tarde"],
                                "SubmissionDateTime": [submission_datetime]
                            })

                            # Carregar dados existentes
                            existing_data_reservations = conn.read(worksheet="Folha")
                            
                            # Remover linhas completamente vazias e resetar o índice
                            existing_data_reservations = existing_data_reservations.dropna(how='all').reset_index(drop=True)

                            # Encontrar o primeiro índice vazio
                            first_empty_index = existing_data_reservations.index[existing_data_reservations.isnull().all(axis=1)].min()
                            
                            if pd.isna(first_empty_index):
                                first_empty_index = len(existing_data_reservations)

                            # Adicionar nova linha no primeiro índice vazio
                            existing_data_reservations.loc[first_empty_index] = new_data.iloc[0]

                            # Atualizar a planilha com os novos dados
                            conn.update(worksheet="Folha", data=existing_data_reservations)

                            st.success("Dados registrados com sucesso!")

            if st.button("😴 Saída Tarde"):
                            # Obter a hora atual
                            current_time = datetime.now()
                            one_hour_after = current_time + timedelta(hours=1)
                            submission_datetime = one_hour_after.strftime("%Y-%m-%d %H:%M:%S")

                            # Criar nova linha com nome, botão e hora
                            new_data = pd.DataFrame({
                                "Name": [nome],
                                "Button": ["Saída Tarde"],
                                "SubmissionDateTime": [submission_datetime]
                            })

                            # Carregar dados existentes
                            existing_data_reservations = conn.read(worksheet="Folha")
                            
                            # Remover linhas completamente vazias e resetar o índice
                            existing_data_reservations = existing_data_reservations.dropna(how='all').reset_index(drop=True)

                            # Encontrar o primeiro índice vazio
                            first_empty_index = existing_data_reservations.index[existing_data_reservations.isnull().all(axis=1)].min()
                            
                            if pd.isna(first_empty_index):
                                first_empty_index = len(existing_data_reservations)

                            # Adicionar nova linha no primeiro índice vazio
                            existing_data_reservations.loc[first_empty_index] = new_data.iloc[0]

                            # Atualizar a planilha com os novos dados
                            conn.update(worksheet="Folha", data=existing_data_reservations)

                            st.success("Dados registrados com sucesso!")
            else:
                st.warning("Pin incorreto.")
        except ValueError:
            st.warning("Utilize somente numeros")                     

"""
with st.form("add_data"):
    new_name = st.text_input("Nome")
    new_button = st.text_input("Botão")
    new_date = st.text_input("data")
    submitted = st.form_submit_button("Adicionar")

    if submitted:
        first_empty_index = df.index[df.isnull().all(axis=1)].min()
        
        if pd.isna(first_empty_index):
            first_empty_index = len(df)
        
        new_data = pd.DataFrame({"Name": [new_name], "Button": [new_button], "SubmissionDateTime":[new_date]})
        
        df.loc[first_empty_index] = new_data.iloc[0]
    
        conn.update(data=df, worksheet="Folha")
        
        st.success("Dados adicionados com sucesso!")
"""