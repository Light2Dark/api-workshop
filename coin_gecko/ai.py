import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA
from sklearn.linear_model import LinearRegression

# response = requests.get("https://api.coingecko.com/api/v3/coins/list?include_platform=true")

# with open("response.json", "w") as f:
#     f.write(response.text)
    
def predict_coin_neural_net(prices_list: list[str]):
    # Define the input and output data
    X = np.array(prices_list[:-1]).reshape(-1, 1)
    y = np.array(prices_list[1:])

    # Create the linear regression model
    model = LinearRegression()

    # Train the model on the input and output data
    model.fit(X, y)

    # Predict the next value in the list
    next_price = model.predict(np.array([prices_list[-1]]).reshape(-1, 1))[0]
    return next_price


def arima():
    # Load the data
    prices = [100, 110, 300, 400]

    # generate a series of 20 large random numbers in increasing order
    prices = np.random.randint(100, 1000, 20)
    prices.sort()

    dates = pd.date_range('2022-01-01', periods=len(prices), freq='D')
    df = pd.DataFrame({'date': dates, 'price': prices})
    df.set_index('date', inplace=True)

    # Plot the time series
    plt.plot(df)
    plt.title('Daily Crypto Prices')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.show()

    # Fit the ARIMA model
    model = ARIMA(df, order=(1, 1, 0))
    results = model.fit()

    # Generate forecasts
    forecast = results.forecast(steps=7)

    # Plot the forecasts
    plt.plot(df, label='Actual')
    plt.plot(forecast, label='Forecast')
    plt.title('ARIMA Forecast')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()
    plt.show()
    
if __name__ == "__main__":
    # predict_coin_neural_net([100, 110, 300, 400])
    from datetime import datetime, date, timedelta
    timestamp_today = int(datetime.now().timestamp())
    timestamp_7daysago = int((datetime.now() - timedelta(days=7)).timestamp())
    print(timestamp_today)
    print(timestamp_7daysago)
    
    readable_time = datetime.fromtimestamp(timestamp_today).strftime('%Y-%m-%d %H:%M:%S')
    print(readable_time)