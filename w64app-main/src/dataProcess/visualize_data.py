import pandas as pd
import matplotlib.pyplot as plt

# Assuming closed_tickets is your DataFrame for tickets that have been closed
def process_closed_tickets(closed_tickets):
  # Ensure that 'data_chiusura' is a datetime column
  closed_tickets['data_modifica'] = pd.to_datetime(closed_tickets['data_modifica'], errors='coerce')
  closed_tickets['data_apertura'] = pd.to_datetime(closed_tickets['data_apertura'], errors='coerce')

  # Avoid SettingWithCopyWarning by using .loc
  closed_tickets.loc[:, 'data_chiusura'] = closed_tickets['data_modifica']  # Assuming 'data_modifica' is the closed date

  # Calculate the resolution time in hours
  closed_tickets.loc[:, 'resolution_time'] = (closed_tickets['data_chiusura'] - closed_tickets['data_apertura']).dt.total_seconds() / 3600

  # Create the 'month_year' column (this will be used for monthly analysis)
  closed_tickets['month_year'] = closed_tickets['data_chiusura'].dt.to_period('M')
  
  return closed_tickets

def analyze_ticket_data(ticket_df, rientri_df, spedizioni_df, materiale_clienti_df):
  # Process closed tickets
  closed_tickets = ticket_df[ticket_df['id_stato'] == 'CHIUSURA']
  closed_tickets = process_closed_tickets(closed_tickets)

  # --- Average Ticket Resolution Time per Operator ---
  print(closed_tickets['operatore_nome'].unique())
  avg_resolution_time = closed_tickets.groupby('operatore_nome')['resolution_time'].mean().reset_index()
  print("\nAverage Ticket Resolution Time per Operator:")
  print(avg_resolution_time)

  # --- Monthly Closed Tickets per Operator ---
  closed_tickets['month_year'] = closed_tickets['data_chiusura'].dt.to_period('M')  # Ensure this is added
  monthly_closed_tickets = closed_tickets.groupby(['operatore_nome', 'month_year']).size().reset_index(name='ticket_count')
  print("\nMonthly Closed Tickets per Operator:")
  print(monthly_closed_tickets)

  # --- Forecast Ticket Count per Client ---
  # Assuming you want a simple linear forecast (this can be expanded with actual forecasting models)
  client_ticket_counts = ticket_df.groupby('cliente_nome').size().reset_index(name='ticket_count')
  plt.bar(client_ticket_counts['cliente_nome'], client_ticket_counts['ticket_count'])
  plt.xlabel('Client')
  plt.ylabel('Ticket Count')
  plt.title('Ticket Count per Client')
  plt.xticks(rotation=90)
  plt.show()

  # --- Visualize Tickets per Problem Type ---
  problem_types = ticket_df['tipo_problema'].value_counts().reset_index()
  problem_types.columns = ['Problem Type', 'Ticket Count']
  plt.bar(problem_types['Problem Type'], problem_types['Ticket Count'])
  plt.xlabel('Problem Type')
  plt.ylabel('Ticket Count')
  plt.title('Tickets per Problem Type')
  plt.xticks(rotation=90)
  plt.show()

  # --- Summarize Total Tickets ---
  ticket_status_summary = ticket_df.groupby('id_stato').size().reset_index(name='ticket_count')
  print("\nTotal Ticket Summary by Status:")
  print(ticket_status_summary)

  # --- Visualize Rientri per Client ---
  rientri_with_clients = rientri_df.merge(ticket_df[['id_ticket', 'cliente_nome']], on='id_ticket', how='left')
  rientri_summary = rientri_with_clients.groupby('cliente_nome').size().reset_index(name='rientri_count')
  plt.bar(rientri_summary['cliente_nome'], rientri_summary['rientri_count'])
  plt.xlabel('Client')
  plt.ylabel('Rientri Count')
  plt.title('Rientri per Client')
  plt.xticks(rotation=90)
  plt.show()

  # --- Visualize Spedizioni per Client ---
  spedizioni_with_clients = spedizioni_df.merge(ticket_df[['id_ticket', 'cliente_nome']], on='id_ticket', how='left')
  spedizioni_summary = spedizioni_with_clients.groupby(['cliente_nome', 'materiale']).size().reset_index(name='spedizioni_count')
  print("\nSpedizioni Summary by Client and Material:")
  print(spedizioni_summary)

  plt.bar(spedizioni_summary['cliente_nome'], spedizioni_summary['spedizioni_count'])
  plt.xlabel('Client')
  plt.ylabel('Spedizioni Count')
  plt.title('Spedizioni per Client')
  plt.xticks(rotation=90)
  plt.show()
