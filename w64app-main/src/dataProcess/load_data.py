from database.query_data import load_data_to_dataframe

def load_all_data():
  # SQL Queries to load data and join tables for additional info
  ticket_query = """
  SELECT 
    t.id_ticket,
    t.id_operatore,
    t.id_cliente,
    t.data_apertura,
    t.data_modifica,
    t.id_istanza,
    t.ticket_ext,
    t.id_stato,
    t.data_segnalazione,
    t.rientro,
    t.tipo_problema,
    t.terze_parti,
    t.spedizione,
    t.intervento,
    t.data_intervento_tkt,
    o.nome AS operatore_nome,
    o.cognome AS operatore_cognome,
    c.descrizione AS cliente_nome,
    g.descrizione AS gruppo_descrizione
  FROM ticket t
  LEFT JOIN operatori o ON t.id_operatore = o.id_operatore
  LEFT JOIN materiale_clienti c ON t.id_cliente = c.id_cliente
  LEFT JOIN gruppi g ON o.id_gruppo = g.id_gruppo;
  """

  rientri_query = """
  SELECT 
    r.id_ticket,
    r.id_rientro,
    r.data_inserimento,
    r.rientro,
    r.id_operatore,
    o.nome AS operatore_nome,
    o.cognome AS operatore_cognome
  FROM rientri r
  LEFT JOIN operatori o ON r.id_operatore = o.id_operatore;
  """

  spedizioni_query = """
  SELECT 
    s.id_ticket,
    s.id_spedizione,
    s.data_inserimento,
    s.spedizione,
    s.materiale,
    s.id_operatore,
    o.nome AS operatore_nome,
    o.cognome AS operatore_cognome
  FROM spedizioni s
  LEFT JOIN operatori o ON s.id_operatore = o.id_operatore;
  """

  materiale_clienti_query = """
  SELECT * FROM materiale_clienti;
  """

  # Load data into DataFrames
  ticket_df = load_data_to_dataframe(ticket_query)
  rientri_df = load_data_to_dataframe(rientri_query)
  spedizioni_df = load_data_to_dataframe(spedizioni_query)
  materiale_clienti_df = load_data_to_dataframe(materiale_clienti_query)

  print("Loaded ", ticket_df.shape[0], " tickets into df")
  print("Loaded ", rientri_df.shape[0], " returns into df")
  print("Loaded ", spedizioni_df.shape[0], " shipments into df")
  print("Loaded ", materiale_clienti_df.shape[0], " clients into df")


  # Return the dataframes
  return ticket_df, rientri_df, spedizioni_df, materiale_clienti_df