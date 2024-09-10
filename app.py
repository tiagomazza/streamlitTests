import streamlit as st
from streamlit_gsheets import GSheetsConnection
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import traceback

st.markdown(
    """
    <!-- Seu CSS personalizado aqui -->
    """,
    unsafe_allow_html=True
)

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

def fill_missing_data(data_frame):
    try:
        default_entry_morning = pd.Timestamp.now().replace(hour=9, minute=0, second=0)
        default_exit_morning = pd.Timestamp.now().replace(hour=12, minute=30, second=0)
        default_entry_afternoon = pd.Timestamp.now().replace(hour=14, minute=30, second=0)
        default_exit_afternoon = pd.Timestamp.now().replace(hour=18, minute=0, second=0)

        for index, row in data_frame.iterrows():
            if pd.isnull(row['Entrada Manhã']):
                data_frame.at[index, 'Entrada Manhã'] = default_entry_morning
            if pd.isnull(row['Saída Manhã']):
                data_frame.at[index, 'Saída Manhã'] = default_exit_morning
            if pd.isnull(row['Entrada Tarde']):
                data_frame.at[index, 'Entrada Tarde'] = default_entry_afternoon
            if pd.isnull(row['Saída Tarde']):
                data_frame.at[index, 'Saída Tarde'] = default_exit_afternoon
    except Exception as e:
        st.error(f"Erro ao preencher dados faltantes: {e}")
        st.error(traceback.format_exc())

def save_to_new_sheet(df, sheet_name="exportado"):
    try:
        try:
            existing_data = conn.read(worksheet=sheet_name, ttl=5)
        except Exception:
            existing_data = None

        if existing_data is None:
            conn.create(worksheet=sheet_name)

        df_dict = df.to_dict(orient="records")
        conn.update(worksheet=sheet_name, data=df_dict)
        st.success(f"Dados salvos na aba '{sheet_name}' com sucesso.")
    except Exception as e:
        st.error(f"Erro ao salvar dados na aba '{sheet_name}': {e}")
        st.error(traceback.format_exc())

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
                    ("☕ Entrada Manhã", "Entrada Manhã"),
                    ("🌮 Saída Manhã", "Saída Manhã"),
                    ("🌄 Entrada Tarde", "Entrada Tarde"),
                    ("😴 Saída Tarde", "Saída Tarde")
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

elif pagina_selecionada == "🔍Consultas":
    st.title("🔍Consulta")
    
    nomes = existing_data_reservations["Name"].unique()
    filtro_nome = st.selectbox("Filtrar por Nome", ["Todos"] + list(nomes))
    data_inicio = st.date_input("Data de Início")
    data_fim = st.date_input("Data de Fim")

    try:
        filtered_data = existing_data_reservations.copy()
        if filtro_nome != "Todos":
            filtered_data = filtered_data[filtered_data["Name"] == filtro_nome]
        if data_inicio and data_fim:
            data_inicio = datetime.combine(data_inicio, datetime.min.time())
            data_fim = datetime.combine(data_fim, datetime.max.time())
            filtered_data["SubmissionDateTime"] = pd.to_datetime(filtered_data["SubmissionDateTime"])
            filtered_data = filtered_data[(filtered_data["SubmissionDateTime"] >= data_inicio) & (filtered_data["SubmissionDateTime"] <= data_fim)]

        data = {
            'Data': filtered_data['SubmissionDateTime'].dt.strftime("%d/%m"),
            'Nome': filtered_data['Name'],
            'Entrada Manhã': np.where(filtered_data['Button'] == 'Entrada Manhã', filtered_data['SubmissionDateTime'].dt.strftime("%H:%M"), pd.NaT),
            'Saída Manhã': np.where(filtered_data['Button'] == 'Saída Manhã', filtered_data['SubmissionDateTime'].dt.strftime("%H:%M"), pd.NaT),
            'Entrada Tarde': np.where(filtered_data['Button'] == 'Entrada Tarde', filtered_data['SubmissionDateTime'].dt.strftime("%H:%M"), pd.NaT),
            'Saída Tarde': np.where(filtered_data['Button'] == 'Saída Tarde', filtered_data['SubmissionDateTime'].dt.strftime("%H:%M"), pd.NaT),
            'Total trabalhado': pd.NaT
        }
        df = pd.DataFrame(data)

        for col in ['Entrada Manhã', 'Saída Manhã', 'Entrada Tarde', 'Saída Tarde']:
            df[col] = pd.to_datetime(df[col])

        grouped_data = df.groupby(['Data', 'Nome']).agg({
            'Entrada Manhã': 'first',
            'Saída Manhã': 'first',
            'Entrada Tarde': 'first',
            'Saída Tarde': 'first'
        }).reset_index()

        grouped_data['Total trabalhado'] = np.nan
        for index, row in grouped_data.iterrows():
            if not (pd.isnull(row['Entrada Manhã']) or pd.isnull(row['Saída Manhã']) or 
                    pd.isnull(row['Entrada Tarde']) or pd.isnull(row['Saída Tarde'])):
                total_trabalhado = (row['Saída Manhã'] - row['Entrada Manhã']) + (row['Saída Tarde'] - row['Entrada Tarde'])
                grouped_data.at[index, 'Total trabalhado'] = total_trabalhado

        grouped_data['Total trabalhado'] = grouped_data['Total trabalhado'].apply(lambda x: x.total_seconds() / 3600 if pd.notnull(x) else 0)
        grouped_data['Total trabalhado'] = grouped_data['Total trabalhado'].apply(lambda x: '{:02.0f}:{:02.0f}'.format(*divmod(x * 60, 60)))

        for col in ['Entrada Manhã', 'Saída Manhã', 'Entrada Tarde', 'Saída Tarde']:
            grouped_data[col] = grouped_data[col].dt.strftime("%H:%M")

        st.write(grouped_data)

        sheet_name = st.text_input("Digite o nome da nova aba:", "Nova_aba")
        if st.button("Salvar dados"):
            save_to_new_sheet(grouped_data, sheet_name)

        st.write("[Aceder a planilha](https://docs.google.com/spreadsheets/d/1ujI1CUkvZoAYuucX4yrV2Z5BN3Z8-o-Kqm3PAfMqi0I/edit?gid=1541275584#gid=1541275584)")
        st.write("[Aceder a documentação](https://docs.google.com/document/d/1wgndUW2Xb48CBi6BSgSBRVw2sdqgqFtZxg_9Go5GYLg/edit?usp=sharing)")

    except Exception as e:
        st.error(f"Erro ao processar dados de consulta: {e}")
        st.error(traceback.format_exc())

elif pagina_selecionada == "🔐Restrito":
    st.title("🔐Restrito")
    # Implementação da página restrita aqui (similar à página de Consultas)
    # ...

try:
    entered_password = str(int(st.sidebar.text_input("", type="password")))
except ValueError:
    st.sidebar.warning("Senha deve conter apenas números")