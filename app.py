import streamlit as st
from streamlit_gsheets import GSheetsConnection
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import traceback

try:
    conn = st.connection("gsheets", type=GSheetsConnection)
    st.success("Conexão com Google Sheets estabelecida com sucesso.")
except Exception as e:
    st.error(f"Erro ao conectar com Google Sheets: {e}")
    st.error(traceback.format_exc())

def load_existing_data(worksheet_name):
    try:
        existing_data = conn.read(worksheet=worksheet_name, ttl=5)
        return existing_data.dropna(how="all")
    except Exception as e:
        st.error(f"Erro ao carregar dados da planilha '{worksheet_name}': {e}")
        st.error(traceback.format_exc())
        return pd.DataFrame()


# Interface do usuário
st.sidebar.image("https://aborgesdoamaral.pt/wp-content/uploads/2021/04/marca-de-75-anos.png", use_column_width=True)
pagina_selecionada = st.sidebar.radio("", ["✍🏽Marcação de Ponto", "🔍Consultas", "🔐Restrito"])

try:
    dados = conn.read(worksheet="Dados", usecols=["Pin", "Nome"], ttl=5)
    admin_row = dados.loc[dados["Nome"] == "Admin"]
    senha_admin = str(int(admin_row["Pin"].iloc[0])) if not admin_row.empty else None
except Exception as e:
    st.error(f"Erro ao carregar dados de administrador: {e}")
    st.error(traceback.format_exc())

existing_data_reservations = load_existing_data("Folha")

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
                st.write("")

                for button_text, button_name in [
                    ("☕ Entrada Manhã", "Entrada Manhã")

                ]:
                    if st.button(button_text):
                        try:
                            submission_datetime = (datetime.now() + timedelta(hours=1)).strftime("%Y-%m-%d %H:%M:%S")
                            new_row = {"Name": nome, "Button": button_name, "SubmissionDateTime": submission_datetime}
                            new_rows = existing_data_reservations.to_dict(orient="records")
                            new_rows.append(new_row)
                            conn.update(worksheet="Folha", data=new_rows)
                            st.success("Dados registrados com sucesso!")
                        except Exception as e:
                            st.error(f"Erro ao registrar {button_name}: {e}")
                            st.error(traceback.format_exc())
            else:
                st.warning("Pin incorreto.")
        except ValueError:
            st.warning("Utilize somente números")
        except Exception as e:
            st.error(f"Erro inesperado: {e}")
            st.error(traceback.format_exc())

try:
    entered_password = str(int(st.sidebar.text_input("", type="password")))
except ValueError:
    st.sidebar.warning("Senha deve conter apenas números")