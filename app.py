
import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

st.markdown(
    """
    <style>
    /* Altera a cor de fundo e a cor do texto do campo de entrada */
    .stTextInput>div>div>input {
        background-color: #ffcccb; /* Cor de fundo desejada */
        color: #000000; /* Cor do texto desejada */
    }
    </style>
    """,
    unsafe_allow_html=True
)

#pagina_selecionada = st.sidebar.radio("", ["✍🏽Marcação de Ponto"])

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
""""
# Lê os dados existentes
df = conn.read(
    worksheet="Folha",
    ttl="0m",
    usecols=[0,1,2]
)

df = df.dropna(how='all').reset_index(drop=True)

def load_existing_data(worksheet_name):
    existing_data = conn.read(worksheet=worksheet_name, ttl=5)
    return existing_data.dropna(how="all")

def fill_missing_data(data_frame):
    default_entry_morning = pd.Timestamp.now().replace(hour=9, minute=0, second=0)
    default_exit_morning = pd.Timestamp.now().replace(hour=12, minute=30, second=0)
    default_entry_afternoon = pd.Timestamp.now().replace(hour=14, minute=30, second=0)
    default_exit_afternoon = pd.Timestamp.now().replace(hour=18, minute=0, second=0)


def save_to_new_sheet(df, sheet_name="exportado"):
    try:
        # Verifica se a aba já existe
        try:
            existing_data = conn.read(worksheet=sheet_name, ttl=5)
        except Exception:
            existing_data = None
        
        # Se não existir, cria a aba
        if existing_data is None:
            conn.create(worksheet=sheet_name)

        # Converte DataFrame para dicionário
        df_dict = df.to_dict(orient="records")
        print("DataFrame convertido para dicionário:", df_dict)  # Adicionado para depuração

        # Atualiza a aba com os dados
        conn.update(worksheet=sheet_name, data=df_dict)
        print("Dados atualizados na nova aba.")  # Adicionado para depuração

        st.success(f"Dados salvos na aba '{sheet_name}' com sucesso.")
    except Exception as e:
        st.error(f"Erro ao salvar dados na aba '{sheet_name}': {e}")
st.sidebar.image("https://aborgesdoamaral.pt/wp-content/uploads/2021/04/marca-de-75-anos.png", use_column_width=True)  # 
"""
pagina_selecionada = st.sidebar.radio("", ["✍🏽Marcação de Ponto", "🔍Consultas", "🔐Restrito"])

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

                # Dar as boas-vindas utilizando o nome correspondente
                st.write(f"😀 Bem-vindo, {nome}!")

                # Adicionar espaço entre a mensagem de boas-vindas e os botões
                st.write("")

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

