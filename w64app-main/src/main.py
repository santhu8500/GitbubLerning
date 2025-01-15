from dataProcess.load_data import load_all_data
from dataProcess.visualize_data import analyze_ticket_data
from dataProcess.forecast_tickets import forecast_tickets

ticket_df, rientri_df, spedizioni_df, materiale_clienti_df = load_all_data()

# Display the first few rows of each DataFrame for verification
print("Ticket DataFrame:")
print(ticket_df.head())

print("\nRientri DataFrame:")
print(rientri_df.head())

print("\nSpedizioni DataFrame:")
print(spedizioni_df.head())

# Analyze data
analyze_ticket_data(ticket_df, rientri_df, spedizioni_df, materiale_clienti_df)

# Forecast ticket counts for the next 4 weeks
forecasted_tickets = forecast_tickets(ticket_df, weeks_to_forecast=12)