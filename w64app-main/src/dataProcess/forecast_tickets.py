from prophet import Prophet
import pandas as pd
import matplotlib.pyplot as plt

# Function to preprocess ticket data and aggregate by week
def preprocess_ticket_data(ticket_df):
    ticket_df['data_apertura'] = pd.to_datetime(ticket_df['data_apertura'])
    ticket_df.set_index('data_apertura', inplace=True)
    weekly_ticket_counts = ticket_df.resample('W').size()  # Aggregate weekly ticket count
    weekly_ticket_counts = weekly_ticket_counts.asfreq('W', fill_value=0)
    return weekly_ticket_counts

# Function for forecasting using Prophet
def forecast_ticket_counts(weekly_ticket_counts, weeks_to_forecast=1):
    # Prepare the data for Prophet
    df = weekly_ticket_counts.reset_index()
    df.columns = ['ds', 'y']  # Prophet requires columns named 'ds' (date) and 'y' (value)

    # Initialize Prophet and fit the model
    model = Prophet(yearly_seasonality=True, weekly_seasonality=True)
    model.fit(df)

    # Create a future dataframe for predictions
    future = model.make_future_dataframe(periods=weeks_to_forecast, freq='W')

    # Forecast future values
    forecast = model.predict(future)

    # Extract the forecasted values
    forecast_df = forecast[['ds', 'yhat']].tail(weeks_to_forecast)
    forecast_df.set_index('ds', inplace=True)
    forecast_df.rename(columns={'yhat': 'forecast'}, inplace=True)

    return forecast_df

# Function to plot historical data and forecasted values
def plot_forecast(weekly_ticket_counts, forecast_df):
    plt.figure(figsize=(10, 6))
    plt.plot(weekly_ticket_counts.index, weekly_ticket_counts, label='Historical Data', color='blue')
    plt.plot(forecast_df.index, forecast_df['forecast'], label='Forecasted Data', color='red', linestyle='--')
    plt.fill_between(forecast_df.index, 0, forecast_df['forecast'], color='red', alpha=0.2)
    plt.title('Ticket Forecast for the Coming Weeks')
    plt.xlabel('Date')
    plt.ylabel('Number of Tickets')
    plt.legend()
    plt.grid(True)
    plt.show()

# Main function to load data, preprocess, forecast, and visualize
def forecast_tickets(ticket_df, weeks_to_forecast):
    weekly_ticket_counts = preprocess_ticket_data(ticket_df)
    forecast_df = forecast_ticket_counts(weekly_ticket_counts, weeks_to_forecast)

    print("Forecasted Weeks and Ticket Counts:")
    print(forecast_df)
    
    plot_forecast(weekly_ticket_counts, forecast_df)
    return forecast_df
