                if st.button("Press here"):
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
