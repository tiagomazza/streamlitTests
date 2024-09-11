'''import pandasql as psql
import streamlit as st

st.subheader("📗 Google Sheets st.connection using Service Account")

st.write("#### 1. API Reference")
with st.echo():
    import streamlit as st

    from streamlit_gsheets import GSheetsConnection

    conn = st.connection("gsheets", type=GSheetsConnection)
    st.write(conn)
    st.help(conn)

docs_url = (
    "https://docs.streamlit.io/streamlit-community-cloud/get-started/"
    "deploy-an-app/connect-to-data-sources/secrets-management"
)

st.write("#### 2. Initial setup")
st.markdown(
    f"""
## Initial setup for CRUD mode

1. Setup `.streamlit/secrets.toml` inside your Streamlit app root directory,
check out [Secret management documentation]({docs_url}) for references.

2. [Enable API Access for a
Project](https://docs.gspread.org/en/v5.7.1/oauth2.html#enable-api-access-for-a-project)
    * Head to [Google Developers Console](https://console.developers.google.com/) and
      create a new project (or select the one you already have).
    * In the box labeled “Search for APIs and Services”, search for “Google Drive API”
      and enable it.
    * In the box labeled “Search for APIs and Services”, search for “Google Sheets API”
      and enable it.
3. [Using Service
   Account](https://docs.gspread.org/en/v5.7.1/oauth2.html#for-bots-using-service-account)
    * Enable API Access for a Project if you haven't done it yet.
    * Go to “APIs & Services > Credentials” and choose “Create credentials > Service
      account key”.
    * Fill out the form
    * Click “Create” and “Done”.
    * Press “Manage service accounts” above Service Accounts.
    * Press on ⋮ near recently created service account and select “Manage keys” and then
      click on “ADD KEY > Create new key”.
    * Select JSON key type and press “Create”.

You will automatically download a JSON file with credentials. It may look like this:
```
{{
    "type": "service_account",
    "project_id": "api-project-XXX",
    "private_key_id": "2cd … ba4",
    "private_key": "-----BEGIN PRIVATE KEY-----\\nNrDyLw … jINQh/9\\n-----END PRIVATE KEY-----\\n",
    "client_email": "473000000000-yoursisdifferent@developer.gserviceaccount.com",
    "client_id": "473 … hd.apps.googleusercontent.com",
    ...
}}
```
Remember the path to the downloaded credentials file. Also, in the next step you'll need
the value of client_email from this file.

* **:red[Very important!]** Go to your
spreadsheet and share it with a client_email from the step above. Just like you do with
any other Google account. If you don't do this, you'll get a
`gspread.exceptions.SpreadsheetNotFound` exception when trying to access this
spreadsheet from your application or a script.

4. Inside `streamlit/secrets.toml` place `service_account` configuration from downloaded
   JSON file, in the following format (where `gsheets` is your `st.connection` name):

```
# .streamlit/secrets.toml
[connections.gsheets]
spreadsheet = "<spreadsheet-name-or-url>"

# worksheet GID is used when using Public Spreadsheet URL, when using service_account
# it will be picked as folder_id
worksheet = "<worksheet-gid-or-folder-id>"

# leave empty when using Public Spreadsheet URL, when using
# service_account -> type = "service_account"
type = ""

project_id = ""
private_key_id = ""
private_key = ""
client_email = ""
client_id = ""
auth_uri = ""
token_uri = ""
auth_provider_x509_cert_url = ""
client_x509_cert_url = ""
```

"""
)

st.write("#### 3. Load DataFrame into Google Sheets")

with st.echo():
    import streamlit as st

    from streamlit_gsheets import GSheetsConnection

    # Create GSheets connection
    conn = st.connection("gsheets", type=GSheetsConnection)

    # Demo Births DataFrame
    df = psql.load_births()

    # click button to update worksheet
    # This is behind a button to avoid exceeding Google API Quota
    if st.button("Create new worksheet"):
        df = conn.create(
            worksheet="Example 1",
            data=df,
        )
        st.cache_data.clear()
        st.rerun()

    # Display our Spreadsheet as st.dataframe
    st.dataframe(df.head(10))


st.write("#### 4. Read Google WorkSheet as DataFrame")
st.info(
    "If the sheet has been deleted, press 'Create new worksheet' button above.",
    icon="ℹ️",  # noqa: RUF001
)

with st.echo():
    import streamlit as st

    from streamlit_gsheets import GSheetsConnection

    # Create GSheets connection
    conn = st.connection("gsheets", type=GSheetsConnection)

    # Read Google WorkSheet as DataFrame
    df = conn.read(
        worksheet="Example 1",
        usecols=[
            0,
            1,
        ],  # specify columns which you want to get, comment this out to get all columns
    )

    # Display our Spreadsheet as st.dataframe
    st.dataframe(df)

st.write("#### 5. Update Google WorkSheet using DataFrame")
with st.echo():
    import streamlit as st

    from streamlit_gsheets import GSheetsConnection

    # Create GSheets connection
    conn = st.connection("gsheets", type=GSheetsConnection)

    # Demo Meat DataFrame
    df = psql.load_meat()

    # click button to update worksheet
    # This is behind a button to avoid exceeding Google API Quota
    if st.button("Update worksheet"):
        df = conn.update(
            worksheet="Example 1",
            data=df,
        )
        st.cache_data.clear()
        st.rerun()

    # Display our Spreadsheet as st.dataframe
    st.dataframe(df.head(10))

st.write("#### 6. Query Google WorkSheet with SQL and get results as DataFrame")
st.info(
    "Mutation SQL queries are in-memory only and do not results in the Worksheet update.",
    icon="ℹ️",  # noqa: RUF001
)


with st.echo():
    import streamlit as st

    from streamlit_gsheets import GSheetsConnection

    # Create GSheets connection
    conn = st.connection("gsheets", type=GSheetsConnection)

    # make sure worksheet name is in double quota "", in our case it's "Example 1"
    # DuckDB SQL dialect is supported
    sql = 'select * from "Example 1"'

    df = conn.query(sql=sql, ttl=3600)

    # Display our SQL query results as st.dataframe
    st.dataframe(df.head(10))

st.write("#### 7. Clear/delete worksheet")
with st.echo():
    import streamlit as st

    from streamlit_gsheets import GSheetsConnection

    # Create GSheets connection
    conn = st.connection("gsheets", type=GSheetsConnection)

    # click button to update worksheet
    # This is behind a button to avoid exceeding Google API Quota
    if st.button("Clear worksheet"):
        conn.clear(worksheet="Example 1")
        st.info("Worksheet Example 1 Cleared!")
        st.cache_data.clear()
        st.rerun()

    # click button to delete worksheet using the underlying gspread API
    # This is behind a button to avoid exceeding Google API Quota
    if st.button("Delete worksheet"):
        spreadsheet = conn.client._open_spreadsheet()  # type: ignore
        worksheet = spreadsheet.worksheet("Example 1")
        spreadsheet.del_worksheet(worksheet)
        st.cache_data.clear()
        st.rerun()

        '''

import streamlit as st
from streamlit_gsheets import GSheetsConnection
from datetime import datetime, timedelta
import pandas as pd
import numpy as np

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

# Conexão com o Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

# Função para carregar os dados existentes da planilha
def load_existing_data(worksheet_name):
    existing_data = conn.read(worksheet=worksheet_name, ttl=5)
    return existing_data.dropna(how="all")

def fill_missing_data(data_frame):
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
pagina_selecionada = st.sidebar.radio("", ["✍🏽Marcação de Ponto", "🔍Consultas", "🔐Restrito"])


dados = conn.read(worksheet="Dados", usecols=["Pin", "Nome"], ttl=5)

admin_row = dados.loc[dados["Nome"] == "Admin"]
if not admin_row.empty:
    senha_admin =  str(int(admin_row["Pin"].iloc[0]))
else:
    senha_admin = None


# Carregar dados existentes
existing_data_reservations = load_existing_data("Folha")

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
                
                # Dar as boas-vindas utilizando o nome correspondente
                st.write(f"😀 Bem-vindo, {nome}!")

                # Adicionar espaço entre a mensagem de boas-vindas e os botões
                st.write("")

                if st.button("☕ Entrada Manhã"):
                    # Obter a hora atual
                    submission_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    current_time = datetime.now()
                    one_hour_after = current_time + timedelta(hours=1)
                    submission_datetime = one_hour_after.strftime("%Y-%m-%d %H:%M:%S")

                    # Criar nova linha com nome, botão e hora
                    new_row = {"Name": nome, "Button": "Entrada Manhã", "SubmissionDateTime": submission_datetime}

                    # Adicionar nova linha aos dados existentes
                    new_rows = existing_data_reservations.to_dict(orient="records")
                    new_rows.append(new_row)

                    # Atualizar a planilha com os novos dados
                    conn.update(worksheet="Folha", data=new_rows)

                    st.success("Dados registrados com sucesso!")

                if st.button("🌮 Saída Manhã"):
                    # Obter a hora atual
                    submission_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    current_time = datetime.now()
                    one_hour_after = current_time + timedelta(hours=1)
                    submission_datetime = one_hour_after.strftime("%Y-%m-%d %H:%M:%S")
                    
                    # Criar nova linha com nome, botão e hora
                    new_row = {"Name": nome, "Button": "Saída Manhã", "SubmissionDateTime": submission_datetime}

                    # Adicionar nova linha aos dados existentes
                    new_rows = existing_data_reservations.to_dict(orient="records")
                    new_rows.append(new_row)

                    # Atualizar a planilha com os novos dados
                    conn.update(worksheet="Folha", data=new_rows)

                    st.success("Dados registrados com sucesso!")

                if st.button("🌄 Entrada Tarde"):
                    # Obter a hora atual
                    submission_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    current_time = datetime.now()
                    one_hour_after = current_time + timedelta(hours=1)
                    submission_datetime = one_hour_after.strftime("%Y-%m-%d %H:%M:%S")
                    
                    # Criar nova linha com nome, botão e hora
                    new_row = {"Name": nome, "Button": "Entrada Tarde", "SubmissionDateTime": submission_datetime}

                    # Adicionar nova linha aos dados existentes
                    new_rows = existing_data_reservations.to_dict(orient="records")
                    new_rows.append(new_row)

                    # Atualizar a planilha com os novos dados
                    conn.update(worksheet="Folha", data=new_rows)

                    st.success("Dados registrados com sucesso!")

                if st.button("😴 Saída Tarde"):
                    # Obter a hora atual
                    submission_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    current_time = datetime.now()
                    one_hour_after = current_time + timedelta(hours=1)
                    submission_datetime = one_hour_after.strftime("%Y-%m-%d %H:%M:%S")
                    
                    # Criar nova linha com nome, botão e hora
                    new_row = {"Name": nome, "Button": "Saída Tarde", "SubmissionDateTime": submission_datetime}

                    # Adicionar nova linha aos dados existentes
                    new_rows = existing_data_reservations.to_dict(orient="records")
                    new_rows.append(new_row)

                    # Atualizar a planilha com os novos dados
                    conn.update(worksheet="Folha", data=new_rows)

                    st.success("Dados registrados com sucesso!")
            else:
                st.warning("Pin incorreto.")
        except ValueError:
            st.warning("Utilize somente numeros")

# Página inicial para entrada da senha
try:
    entered_password = str(int(st.sidebar.text_input ("",type="password")))

    if pagina_selecionada == "🔍Consultas":
        st.title("🔍Consulta")
        
        # Filtrar por nome
        nomes = existing_data_reservations["Name"].unique()
        filtro_nome = st.selectbox("Filtrar por Nome", ["Todos"] + list(nomes))

        # Filtrar por data
        data_inicio = st.date_input("Data de Início")
        data_fim = st.date_input("Data de Fim")

        # Filtrar os dados
        filtered_data = existing_data_reservations.copy()

        if filtro_nome != "Todos":
            filtered_data = filtered_data[filtered_data["Name"] == filtro_nome]

        if data_inicio and data_fim:
            data_inicio = datetime.combine(data_inicio, datetime.min.time())
            data_fim = datetime.combine(data_fim, datetime.max.time())
            filtered_data["SubmissionDateTime"] = pd.to_datetime(filtered_data["SubmissionDateTime"])
            filtered_data = filtered_data[(filtered_data["SubmissionDateTime"] >= data_inicio) & (filtered_data["SubmissionDateTime"] <= data_fim)]

        # Criar DataFrame com os dados filtrados
        data = {                                        
            'Data': filtered_data['SubmissionDateTime'].dt.strftime("%d/%m"),  # Formatando para dd/mm
            'Nome': filtered_data['Name'],
            'Entrada Manhã': np.where(filtered_data['Button'] == 'Entrada Manhã', filtered_data['SubmissionDateTime'].dt.strftime("%H:%M"), pd.NaT),
            'Saída Manhã': np.where(filtered_data['Button'] == 'Saída Manhã', filtered_data['SubmissionDateTime'].dt.strftime("%H:%M"), pd.NaT),
            'Entrada Tarde': np.where(filtered_data['Button'] == 'Entrada Tarde', filtered_data['SubmissionDateTime'].dt.strftime("%H:%M"), pd.NaT),
            'Saída Tarde': np.where(filtered_data['Button'] == 'Saída Tarde', filtered_data['SubmissionDateTime'].dt.strftime("%H:%M"), pd.NaT),
            'Total trabalhado': pd.NaT
        }

        df = pd.DataFrame(data)
        df['Entrada Manhã'] = pd.to_datetime(df['Entrada Manhã'])
        df['Saída Manhã'] = pd.to_datetime(df['Saída Manhã'])
        df['Entrada Tarde'] = pd.to_datetime(df['Entrada Tarde'])
        df['Saída Tarde'] = pd.to_datetime(df['Saída Tarde'])

        # Agrupar por data e nome para calcular o total trabalhado por dia
        grouped_data = df.groupby(['Data', 'Nome']).agg({
            'Entrada Manhã': 'first',
            'Saída Manhã': 'first',
            'Entrada Tarde': 'first',
            'Saída Tarde': 'first'
        }).reset_index()

        # Preencher dados faltantes com os horários padrão
        #fill_missing_data(grouped_data)

        # Calcular o total trabalhado por dia
        grouped_data['Total trabalhado'] = np.nan
        for index, row in grouped_data.iterrows():
            if not (pd.isnull(row['Entrada Manhã']) or pd.isnull(row['Saída Manhã']) or pd.isnull(row['Entrada Tarde']) or pd.isnull(row['Saída Tarde'])):
                total_trabalhado = (row['Saída Manhã'] - row['Entrada Manhã']) + (row['Saída Tarde'] - row['Entrada Tarde'])
                grouped_data.at[index, 'Total trabalhado'] = total_trabalhado

        # Converter o total trabalhado para horas e minutos
        grouped_data['Total trabalhado'] = grouped_data['Total trabalhado'].apply(lambda x: x.total_seconds() / 3600 if pd.notnull(x) else 0)
        grouped_data['Total trabalhado'] = grouped_data['Total trabalhado'].apply(lambda x: '{:02.0f}:{:02.0f}'.format(*divmod(x * 60, 60)))

        # Converter as colunas de entrada e saída para o formato hh:mm
        grouped_data['Entrada Manhã'] = grouped_data['Entrada Manhã'].dt.strftime("%H:%M")
        grouped_data['Saída Manhã'] = grouped_data['Saída Manhã'].dt.strftime("%H:%M")
        grouped_data['Entrada Tarde'] = grouped_data['Entrada Tarde'].dt.strftime("%H:%M")
        grouped_data['Saída Tarde'] = grouped_data['Saída Tarde'].dt.strftime("%H:%M")

        # Exibir o DataFrame agrupado na página
        st.write(grouped_data)

        sheet_name = st.text_input("Digite o nome da nova aba:", "Nova_aba")
        if st.button("Salvar dados"):
            save_to_new_sheet(grouped_data)
        st.write(f"[Aceder a planilha](https://docs.google.com/spreadsheets/d/1ujI1CUkvZoAYuucX4yrV2Z5BN3Z8-o-Kqm3PAfMqi0I/edit?gid=1541275584#gid=1541275584)")
        st.write(f"[Aceder a documentação](https://docs.google.com/document/d/1wgndUW2Xb48CBi6BSgSBRVw2sdqgqFtZxg_9Go5GYLg/edit?usp=sharing)")

    elif pagina_selecionada == "🔐Restrito":
      
        st.title("🔐Restrito")

        # Filtrar por nome
        nomes = existing_data_reservations["Name"].unique()
        filtro_nome = st.selectbox("Filtrar por Nome", ["Todos"] + list(nomes))

        # Filtrar por data
        data_inicio = st.date_input("Data de Início")
        data_fim = st.date_input("Data de Fim")

        # Filtrar os dados
        filtered_data = existing_data_reservations.copy()

        if filtro_nome != "Todos":
            filtered_data = filtered_data[filtered_data["Name"] == filtro_nome]

        if data_inicio and data_fim:
            data_inicio = datetime.combine(data_inicio, datetime.min.time())
            data_fim = datetime.combine(data_fim, datetime.max.time())
            filtered_data["SubmissionDateTime"] = pd.to_datetime(filtered_data["SubmissionDateTime"])
            filtered_data = filtered_data[(filtered_data["SubmissionDateTime"] >= data_inicio) & (filtered_data["SubmissionDateTime"] <= data_fim)]

        # Criar DataFrame com os dados filtrados
        data = {
            'Data': filtered_data['SubmissionDateTime'].dt.strftime("%d/%m"),  # Formatando para dd/mm
            'Nome': filtered_data['Name'],
            'Entrada Manhã': np.where(filtered_data['Button'] == 'Entrada Manhã', filtered_data['SubmissionDateTime'].dt.strftime("%H:%M"), pd.NaT),
            'Saída Manhã': np.where(filtered_data['Button'] == 'Saída Manhã', filtered_data['SubmissionDateTime'].dt.strftime("%H:%M"), pd.NaT),
            'Entrada Tarde': np.where(filtered_data['Button'] == 'Entrada Tarde', filtered_data['SubmissionDateTime'].dt.strftime("%H:%M"), pd.NaT),
            'Saída Tarde': np.where(filtered_data['Button'] == 'Saída Tarde', filtered_data['SubmissionDateTime'].dt.strftime("%H:%M"), pd.NaT),
            'Total trabalhado': pd.NaT
        }

        df = pd.DataFrame(data)
        df['Entrada Manhã'] = pd.to_datetime(df['Entrada Manhã'])
        df['Saída Manhã'] = pd.to_datetime(df['Saída Manhã'])
        df['Entrada Tarde'] = pd.to_datetime(df['Entrada Tarde'])
        df['Saída Tarde'] = pd.to_datetime(df['Saída Tarde'])

        # Preencher dados faltantes com os horários padrão
        fill_missing_data(df)

        # Agrupar por data e nome para calcular o total trabalhado por dia
        grouped_data = df.groupby(['Data', 'Nome']).agg({
            'Entrada Manhã': 'first',
            'Saída Manhã': 'first',
            'Entrada Tarde': 'first',
            'Saída Tarde': 'first'
        }).reset_index()

        # Calcular o total trabalhado por dia
        grouped_data['Total trabalhado'] = np.nan
        for index, row in grouped_data.iterrows():
            if not (pd.isnull(row['Entrada Manhã']) or pd.isnull(row['Saída Manhã']) or pd.isnull(row['Entrada Tarde']) or pd.isnull(row['Saída Tarde'])):
                total_trabalhado = (row['Saída Manhã'] - row['Entrada Manhã']) + (row['Saída Tarde'] - row['Entrada Tarde'])
                grouped_data.at[index, 'Total trabalhado'] = total_trabalhado

        # Converter o total trabalhado para horas e minutos
        grouped_data['Total trabalhado'] = grouped_data['Total trabalhado'].apply(lambda x: x.total_seconds() / 3600 if pd.notnull(x) else 0)
        grouped_data['Total trabalhado'] = grouped_data['Total trabalhado'].apply(lambda x: '{:02.0f}:{:02.0f}'.format(*divmod(x * 60, 60)))

        # Converter as colunas de entrada e saída para o formato hh:mm
        grouped_data['Entrada Manhã'] = grouped_data['Entrada Manhã'].dt.strftime("%H:%M")
        grouped_data['Saída Manhã'] = grouped_data['Saída Manhã'].dt.strftime("%H:%M")
        grouped_data['Entrada Tarde'] = grouped_data['Entrada Tarde'].dt.strftime("%H:%M")
        grouped_data['Saída Tarde'] = grouped_data['Saída Tarde'].dt.strftime("%H:%M")

        # Exibir o DataFrame agrupado na página
        st.write(grouped_data)

        sheet_name = st.text_input("Digite o nome da nova aba:", "Nova_aba")
        if st.button("Salvar dados"):
            save_to_new_sheet(grouped_data)

        st.write(f"[Aceder a planilha](https://docs.google.com/spreadsheets/d/1ujI1CUkvZoAYuucX4yrV2Z5BN3Z8-o-Kqm3PAfMqi0I/edit?gid=1541275584#gid=1541275584)")
        st.write(f"[Aceder a documentação](https://docs.google.com/document/d/1wgndUW2Xb48CBi6BSgSBRVw2sdqgqFtZxg_9Go5GYLg/edit?usp=sharing)")

        
except ValueError:
    # Handle invalid input (not an integer)
    print("Invalid password format. Please enter a valid integer.")
    pass
