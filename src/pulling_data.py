import yfinance as yf
import datetime as dt
from datetime import datetime as datetime2
import check_market_status
import daily_bar
import prediction_model
import user_prompt


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
    answer = check_market_status.getIfMakretOpen()
    
    for index, row in data.iterrows():
        date_str = index.date().strftime('%Y-%m-%d')
        if counter >= 1:
            perc_diff = ((row['Close'] - prev_close) / prev_close) * 100
            if perc_diff > 50:
                print("Bad data deteced for stock " + stock + " on date " + date_str + ". Returning to main menu.")
                user_prompt.runQuestion1()
                
                
        counter += 1
        
        today = daily_bar.DailyBar(row['High'], row['Open'], row['Low'], row['Close'], index, row['Volume'])
        if index > testing_date_obj:
            if counter == number_of_rows and answer == "REGULAR":
                prediction_model.predicitionModel(listofdays, date_str, row['Open'], row['Close'], "marketopen")
            else:            
                prediction_model.predicitionModel(listofdays, date_str, row['Open'], row['Close'], "regular")
        listofdays.append(today)
        prev_close = row['Close']
    
    if answer == "CLOSED" or answer == "POST" or answer == "error":
        prediction_model.predicitionModel(listofdays, date_str, row['Open'], row['Close'], "marketclosed")

    print("")
    print("Accuracy percentage for Stock " + stock + " is: " + str((good_score / total_score) * 100) + "%")
    user_prompt.runQuestion1()    