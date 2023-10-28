import sys
import yfinance as yf
import datetime as dt
from datetime import datetime as datetime2
from dateutil.relativedelta import relativedelta
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn import metrics
import requests
import matplotlib.pyplot as plt
import configparser
import hashlib


#---------------------------------------------------------------------------------------------------------
#Creates daily candle bar objects that will be stored in an array later and used in the predicition model.
#---------------------------------------------------------------------------------------------------------
class DailyBar:
    def __init__(self, high, open, low, close, date, volume):
        self.high = high
        self.open = open
        self.low = low
        self.close = close
        self.date = date
        self.volume = volume

    def __str__(self):
        return f"Date: {self.date}, Open: {self.open}, High: {self.high}, Low: {self.low}, Close: {self.close}, Volume: {self.volume}"

#----------------------------------------------------------
#This is how the program tells if the market is open or not
#----------------------------------------------------------

def getIfMakretOpen():
  symbol = "AAPL"
  url = f"https://query1.finance.yahoo.com/v7/finance/options/{symbol}"
  headers = {
      "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36"
  }
  response = requests.get(url, headers=headers)  
  data = response.json()

  if 'optionChain' in data and 'result' in data['optionChain']:
      result = data['optionChain']['result']
      if result and len(result) > 0:
          quote = result[0].get('quote', {})
          market_state = quote.get('marketState')
          return market_state
      else:
          return "error"
  else:
      return "error"

#-------------------------------------------
#images
#-------------------------------------------

def linechart(dailychart, ax):
    # Extracting date and close values from the dailychart objects
    dates = [data.date for data in dailychart]
    close_values = [data.close for data in dailychart]

    # Creating the line chart
    ax.plot(dates, close_values, linestyle='-', color='blue')
    
    # Adding labels and title
    ax.set_xlabel('Date')
    ax.set_ylabel('Close')
    ax.set_title('Daily Close Prices')
    
    # Rotating the x-axis labels for better readability
    ax.tick_params(axis='x', rotation=45)
    


def histogram(n_20_plus, n_0_20_plus,n_0_20_minus, n_20_minus, ax):
    bins2 = [-40,-20,0,20,40]
    returns = []
    
    
    for key, value in n_20_plus.items():
        returns.append(25)    
    for key, value in n_0_20_plus.items():
        returns.append(value)    
    for key, value in n_0_20_minus.items():
        returns.append(value)    
    for key, value in n_20_minus.items():
        returns.append(-25)    
    
    

    ax.hist(returns, bins=bins2, edgecolor='black')

    x_ticks = [-40, -20, 0, 20, 40]  
    
    x_tick_labels = ['<-40%', '-20%', '0%', '20%', '>40%']
    ax.set_xticks(x_ticks)
    ax.set_xticklabels(x_tick_labels)
    
    
    #plt.legend(['n_20_plus', 'n_0_20_plus', 'n_0_20_minus', 'n_20_minus'])
    ax.set_title('Percentage Return Each Year', fontsize=12)
    ax.set_xlabel('Percentage Return')
    ax.set_ylabel('Total Years')
    

def piechart(count_green_year, count_red_year, ax):
    # Prepare data
    labels = ['Green Years', 'Red Years']
    sizes = [count_green_year, count_red_year]
    colors = ['green', 'red']
    
    # Create pie chart
    ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%',
            shadow=True, startangle=90)

    ax.axis('equal')  # Equal aspect ratio ensures a circular pie
    ax.set_title('% of Green/Red Years for last 10 Years', fontsize=12)  # Set chart title

   


#----------------------------------
#getting data and doing descriptive
#----------------------------------

def quantAnalysis(stock):
    company = stock
    current_year_1 = dt.datetime.now().year
    start = dt.datetime(current_year_1 - 10, 1, 1)
    end = dt.datetime.now()
    
    data = yf.download(company, start)
    
    
    first_open_price = 0
    first_open_price_YTD = 0
    first_open_price_30_ago = 0
    
    highest_price = 0
    largest_drawdown = 0
    
    
    current_date = dt.datetime.now().date()
    one_year_ago_temp = current_date - relativedelta(years=1)
    one_year_ago = one_year_ago_temp.replace(day=1)
    thirty_days_ago = current_date - dt.timedelta(days=30)
    current_year = start.year
    current_month = start.month
    each_year_perc_return = {}
    
    green_list_30 = 0
    red_list_30 = 0
    green_list_last_12 = 0
    red_list_last_12 = 0
    month_counter = 0
    dailychart = []
    counter = 0
    
    for index, row in data.iterrows():
    
        date_str = index.date().strftime('%Y-%m-%d')
        if counter >= 1:
            perc_diff = ((row['Close'] - prev_close) / prev_close) * 100
            if perc_diff > 50:
                print("Bad data deteced for stock " + stock + " on date " + date_str + ". Returning to main menu.")
                runQuestion1()
                
        counter += 1
        
        today = DailyBar(row['High'], row['Open'], row['Low'], row['Close'], index, row['Volume'])
        dailychart.append(today)
        
        #this logic handles 10 years lost/gain
        if first_open_price == 0:
            first_open_price = row['Open']
            open_price_year_return = row['Open']
            open_price_prev_month = row['Open']
        latest_close = row['Close']
    
        #this logic handles loss/gain YTD
        if index.year == current_year_1 and first_open_price_YTD == 0:
            first_open_price_YTD = row['Open']
                
        #this logic handles loss/gain last 30 days
        if index.date() > thirty_days_ago:
            if row['Close'] > row['Open']:
                green_list_30 += 1
            else:
                red_list_30 += 1
            if first_open_price_30_ago == 0:
                first_open_price_30_ago = row['Open']        
        
        #this logic handles average return per year
        if index.year != current_year:
            close_price_prev_year = prev_close
            total_gain_loss_for_that_year = ((close_price_prev_year-open_price_year_return) / open_price_year_return) * 100        
            each_year_perc_return.update({current_year:total_gain_loss_for_that_year})        
            open_price_year_return = row['Open']
    
        #This logic will handle the largest drawdown
        if row['High'] > highest_price:
            highest_price = row['High']
            highest_price_date = index.date()
        current_drawdown = ((row['Low'] - highest_price) / highest_price) * 100
        if current_drawdown < largest_drawdown:
            largest_drawdown = current_drawdown
            largest_drawdown_date_start = highest_price_date
            largest_drawdown_date_end = index.date()
    
        #This logic handles how many green/red months in last year
        if index.month != current_month:
            total_gain_loss_for_month = ((prev_close - open_price_prev_month) / open_price_prev_month) * 100
            open_price_prev_month = row['Open']
            if index.date() >= one_year_ago:
                month_counter += 1
                if month_counter != 1:
                  if total_gain_loss_for_month > 0:
                      green_list_last_12 += 1
                  else:
                      red_list_last_12 += 1
            
        current_month = index.month    
        current_year = index.year
        prev_close = row['Close']
        
    
    
    
    
    total_gain_lost_10_year = ((latest_close-first_open_price) / first_open_price) * 100
    total_gain_lost_YTD = ((latest_close-first_open_price_YTD) / first_open_price_YTD) * 100
    total_gain_lost_30_ago = ((latest_close-first_open_price_30_ago) / first_open_price_30_ago) * 100
    
    
    total_sum_returns = sum(each_year_perc_return.values())
    num_values = len(each_year_perc_return)
    average_return_per_year = total_sum_returns / num_values
    
    
    total_green_year_returns = 0
    count_green_year = 0
    total_red_year_returns = 0
    count_red_year = 0
    largest_green_year = 0
    largest_red_year = 0
    n_20_plus = {}
    n_0_20_plus = {}
    n_0_20_minus = {}
    n_20_minus = {}
    
    for key, value in each_year_perc_return.items():
        if value > 0:
            total_green_year_returns += value
            count_green_year += 1
        else:
            total_red_year_returns += value
            count_red_year += 1
        if value > largest_green_year:
            largest_green_year = value
            largest_green_year_year = key
        if value < largest_red_year:
            largest_red_year = value
            largest_red_year_year = key
        
        if value >= 20:
            n_20_plus.update({key:value})
        elif value < 20 and value >= 0:
            n_0_20_plus.update({key:value})    
        elif value < 0 and value > -20:
            n_0_20_minus.update({key:value})    
        elif value <= -20:
            n_20_minus.update({key:value})        
    
    
    if count_green_year > 0:
        average_green_year = total_green_year_returns / count_green_year
    else:
        average_green_year = 0
        
    if count_red_year > 0:
        average_red_year = total_red_year_returns / count_red_year
    else:
        average_red_year = 0
        
    print("\n--------------------------")
    print("Statistics for Stock: " + stock)
    print("--------------------------")
    print("\nGain/Loss YTD:", total_gain_lost_YTD , "%")
    print("Gain/Loss Last 30 days:", total_gain_lost_30_ago , "%")
    print("Gain/Loss Last 10 Years:", total_gain_lost_10_year , "%")
    print("Average Return Per Year:", average_return_per_year , "%")
    print("Average Green Year:", average_green_year , "%")
    print("Average Red Year:", average_red_year , "%")
    print("Largest Green Year:", largest_green_year , "%")
    print("Year of Largest Green Year:", largest_green_year_year)
    print("Largest Red Year:", largest_red_year , "%")
    print("Year of Largest Red Year:", largest_red_year_year)
    print("Largest Drawdown:", largest_drawdown , "%")
    print("Start Date of Largest Drawdown:", largest_drawdown_date_start)
    print("End Date of Largest Drawdown:", largest_drawdown_date_end)
    print("\n\nClick \"X\" on top right of matplotlib image to continue.")
    
    
    fig, axs = plt.subplots(1, 3, figsize=(15, 5))
    fig.suptitle("Quantitave Analysis for Stock: " + stock)
    
    linechart(dailychart, axs[0])
    histogram(n_20_plus, n_0_20_plus,n_0_20_minus, n_20_minus, axs[1])
    piechart(count_green_year, count_red_year, axs[2])
    
    plt.tight_layout()
    plt.show()
    runQuestion1()
    
        

#---------------------------------------
#AI/ML
#---------------------------------------
def predicitionModelDataPull(stock):
    global good_score
    global total_score
    company = stock

    training_date = '2013-01-01'
    training_date_obj = datetime2.strptime(training_date, "%Y-%m-%d")

    end = dt.datetime.now()
    testing_date = '2023-01-01'
    testing_date_obj = datetime2.strptime(testing_date, "%Y-%m-%d")
    listofdays = []
    good_score = 0 
    total_score = 0
    
    counter = 0
    data = yf.download(company, training_date_obj)
    
    number_of_rows = len(data)
    answer = getIfMakretOpen()
    
    for index, row in data.iterrows():
        date_str = index.date().strftime('%Y-%m-%d')
        if counter >= 1:
            perc_diff = ((row['Close'] - prev_close) / prev_close) * 100
            if perc_diff > 50:
                print("Bad data deteced for stock " + stock + " on date " + date_str + ". Returning to main menu.")
                runQuestion1()
                
                
        counter += 1
        
        today = DailyBar(row['High'], row['Open'], row['Low'], row['Close'], index, row['Volume'])
        if index > testing_date_obj:
            if counter == number_of_rows and answer == "REGULAR":
                predicitionModel(listofdays, date_str, row['Open'], row['Close'], "marketopen")
            else:            
                predicitionModel(listofdays, date_str, row['Open'], row['Close'], "regular")
        listofdays.append(today)
        prev_close = row['Close']
    
    if answer == "CLOSED" or answer == "POST" or answer == "error":
        predicitionModel(listofdays, date_str, row['Open'], row['Close'], "marketclosed")

    print("")
    print("Accuracy percentage for Stock " + stock + " is: " + str((good_score / total_score) * 100) + "%")
    runQuestion1()    


def predicitionModel(training_data, date,open,close, type):
    global good_score
    global total_score
    # Extract the training features and labels from the training_data
    training_features = [[bar.close, bar.high, bar.open, bar.low, bar.volume] for bar in training_data]
    training_labels = ['green' if bar.close > bar.open else 'red' for bar in training_data]

    
    clf = DecisionTreeClassifier()
    clf.fit(training_features, training_labels)

    # Extract the features of the last bar in the training_data (current day's features)
    recent_features = training_features[-100:]

    # Predict the label for the next trading day (2020-01-02)
    next_day_prediction = clf.predict(recent_features)
    
    diff = close - open
    if diff > 0:
        answer = 'green'
    else:
        answer = 'red'
    
    if type == "regular":
        if answer == next_day_prediction[0]:
            good_score = good_score + 1
        total_score = total_score + 1
        
    if type == "marketopen":
        print("Prediction for {:<18} {:<20} Answer: {:<20}".format(str(date) + ":", next_day_prediction[0], "Unknown, because market is still open."))
    elif type == "regular":
        print("Prediction for {:<18} {:<20} Answer: {:<20}".format(str(date) + ":", next_day_prediction[0], answer))
    elif type == "marketclosed":
        print("Prediction for {:<18} {:<20} Answer: {:<20}".format("Next Trading Day:", next_day_prediction[0], "Unknown"))
    


#----------------------------------------
#User interface
#----------------------------------------
print("\n\n----------------------------------------------------------------------------")
print("Welcome to our Stock Market Solution that uses Quantitave Analysis and AI/ML.")
print("----------------------------------------------------------------------------\n\n")

    
    
def runQuestion1():
    answer = input("\n\nEnter stock to view analysis for. Please type the ticker symbol for stock in CAPS, Only availabe stocks currently are(TSLA,AMZN,NFLX,MSFT,AAPL,GOOG). Or type \"q\" to quit.\n\n>")
    if answer == "TSLA" or answer == "NFLX" or answer == "AMZN" or answer == "MSFT" or answer == "AAPL" or answer == "GOOG":
        runQuestion2(answer)
    elif answer == "q":
        print("Program ended.")
        sys.exit()
    else:
        print("\n\nIm sorry I dont think I understood that. Please try and answer again")
        runQuestion1()

def runQuestion2(stock):
    answer = input("\n\nSelect what type of analysis you would like to peform on " + stock + "? Please choose one of the options below by typing the letter next to that option. Case sensitive\n\na - Prediction model using AI/ML\nb - Quantitave Analysis\nr - Return to Main Menu\n\n>")
    if answer == "a":
        predicitionModelDataPull(stock)
    elif answer == "b":
        quantAnalysis(stock)
    elif answer == "r":
        runQuestion1()
    else:
        print("\n\nIm sorry I dont think I understood that. Please try and answer again")
        runQuestion2(stock)

total_score = 0
good_score = 0
runQuestion1()












