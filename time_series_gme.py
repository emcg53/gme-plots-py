import requests
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt

#my_api_key = ""    Input your AlphaVenture API key as a str() var here
my_stock = "GME"    
my_timeframe = "TIME_SERIES_DAILY"
response = requests.get("https://www.alphavantage.co/query?function="+my_timeframe+"&symbol="+my_stock+"&outputsize=full&apikey="+my_api_key)
my_response = response.json()

my_response.keys() ## keys are 'Meta Data', 'Time Series (Daily)'. It's a dictionary of dictionaries.
time_series_data = my_response['Time Series (Daily)']


## Put the data I want into a list of lists
my_list = []

for key, value in time_series_data.items():
    my_list.append([key, float(value['1. open']), float(value['2. high']), float(value['3. low']), float(value['4. close'])])

## Add some column names and turn it into a Pandas dataframe
col_names = ["Date", "Open", "High", "Low", "Close"]
my_data = pd.DataFrame(my_list, columns= col_names)

## Subset only data from mid-November 2020 onwards
my_data = my_data[my_data['Date'] >= '2020-11-15']

## Reformat dataframe columns into variables (just because)
x = [dt.datetime.strptime(i, '%Y-%m-%d').date() for i in my_data['Date']]
y_open = my_data['Open']
y_high = my_data['High']
y_low = my_data['Low']
y_close = my_data['Close']

## First plot
## Let's see $GME's Open, High, Low, and Close values over time
plt.plot(x, y_open, label = "Open")
plt.plot(x, y_high, label = "High")
plt.plot(x, y_low, label = "Low")
plt.plot(x, y_close, label = "Close")
plt.ylabel('$ Value')
plt.title('$GME')
plt.legend()
plt.show()


## I want to see how $GME's daily movement (increase/decrease from Open to Close) looks over time
## Add in some horizontal lines at $20 and $-20 to mark big jumps
## Highlight values above/below $20/-20 in yellow to call them out
y_daily_move = my_data['Open']-my_data['Close']
y_daily_20_subset = [i for i in y_daily_move if i < -20 or i > 20]
x_daily_20_subset = [x[i] for i in range(0, len(y_daily_move)) if y_daily_move[i] < -20 or y_daily_move[i] > 20]
plt.scatter(x, y_daily_move, label = 'Diff. Open to Close')
plt.scatter(x_daily_20_subset, y_daily_20_subset, color = 'yellow')
plt.axhline(y=20, color = 'r', linestyle = 'dashed')
plt.axhline(y=-20, color = 'r', linestyle = 'dashed')
plt.ylabel('$ Difference')
plt.title('GME Difference from Open to Close ($)')
plt.show()


## I want to see the difference between $GME's high's and low's each day
## If you don't like stomaching daily stock volatility, you'd want this chart to be clustered around the same values
## I'll call out days where there's over $20 between a daily high and low, which is pretty insane
y_daily_var = my_data['High']-my_data['Low']
y_daily_20_subset = [i for i in y_daily_var if i < -20 or i > 20]
x_daily_20_subset = [x[i] for i in range(0, len(y_daily_var)) if  y_daily_var[i] > 20]
plt.scatter(x, y_daily_var, label = 'Diff. High to Low')
plt.scatter(x_daily_20_subset, y_daily_20_subset, color = 'yellow')
plt.axhline(y=20, color = 'r', linestyle = 'dashed')
plt.ylabel('$ Difference')
plt.title('GME Difference from High to Low ($)')
plt.show()

