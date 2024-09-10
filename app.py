import streamlit as st
from streamlit_gsheets import GSheetsConnection
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import traceback

# Conexão com o Google Sheets
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
    st.success("Conexão com Google Sheets estabelecida com sucesso.")
except Exception as e:
    st.error(f"Erro ao conectar com Google Sheets: {e}")
    st.error(traceback.format_exc())

# Função para carregar os dados existentes da planilha
def load_existing_data(worksheet_name):
    try:
        existing_data = conn.read(worksheet=worksheet_name, ttl=5)
        return existing_data.dropna(how="all")
    except Exception as e:
        st.error(f"Erro ao carregar dados da planilha '{worksheet_name}': {e}")
        st.error(traceback.format_exc())
        return pd.DataFrame()

# Função para atualizar a planilha
def update_sheet(worksheet, data):
    try:
        conn.update(worksheet=worksheet, data=data)
        st.success(f"Dados atualizados na planilha '{worksheet}' com sucesso.")
    except Exception as e:
        st.error(f"Erro ao atualizar a planilha '{worksheet}': {e}")
        st.error(traceback.format_exc())

# Código para marcação de ponto
if pagina_selecionada == "✍🏽Marcação de Ponto":
    st.title("✍🏽Marcação de Ponto")
    pin_digitado = st.text_input("Digite o seu PIN:")
    
    if str(pin_digitado):
        try:
            dados = conn.read(worksheet="Dados", usecols=["Pin", "Nome"], ttl=5)
            pin_int = int(float(pin_digitado))
            
            if pin_int in dados["Pin"].tolist():
                nome = dados.loc[dados["Pin"] == pin_int, "Nome"].iloc[0]
                st.write(f"😀 Bem-vindo, {nome}!")
                
                if st.button("☕ Entrada Manhã"):
                    try:
                        submission_datetime = (datetime.now() + timedelta(hours=1)).strftime("%Y-%m-%d %H:%M:%S")
                        new_row = {"Name": nome, "Button": "Entrada Manhã", "SubmissionDateTime": submission_datetime}
                        
                        existing_data_reservations = load_existing_data("Folha")
                        new_rows = existing_data_reservations.to_dict(orient="records")
                        new_rows.append(new_row)
                        
                        update_sheet("Folha", new_rows)
                    except Exception as e:
                        st.error(f"Erro ao registrar entrada da manhã: {e}")
                        st.error(traceback.format_exc())
                
                # Adicione tratamentos de erro semelhantes para os outros botões
            
            else:
                st.warning("Pin incorreto.")
        except ValueError:
            st.warning("Utilize somente números")
        except Exception as e:
            st.error(f"Erro inesperado: {e}")
            st.error(traceback.format_exc())

# Código para salvar em nova aba
def save_to_new_sheet(df, sheet_name="exportado"):
    try:
        try:
            existing_data = conn.read(worksheet=sheet_name, ttl=5)
        except Exception:
            existing_data = None
        
        if existing_data is None:
            conn.create(worksheet=sheet_name)
        
        df_dict = df.to_dict(orient="records")
        print("DataFrame convertido para dicionário:", df_dict)
        
        update_sheet(sheet_name, df_dict)
    except Exception as e:
        st.error(f"Erro ao salvar dados na aba '{sheet_name}': {e}")
        st.error(traceback.format_exc())

# Na página de consultas
if pagina_selecionada == "🔍Consultas":
    # ... (código de filtragem e processamento)
    
    if st.button("Salvar dados"):
        try:
            save_to_new_sheet(grouped_data, sheet_name)
        except Exception as e:
            st.error(f"Erro ao salvar dados: {e}")
            st.error(traceback.format_exc())