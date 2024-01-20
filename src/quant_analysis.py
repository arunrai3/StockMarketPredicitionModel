import yfinance as yf
import datetime as dt
from dateutil.relativedelta import relativedelta
import daily_bar
import matplotlib.pyplot as plt
import line_chart
import histogram as histogram2
import pie_chart
import user_prompt


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
                user_prompt.runQuestion1()
                
        counter += 1
        
        today = daily_bar.DailyBar(row['High'], row['Open'], row['Low'], row['Close'], index, row['Volume'])
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
    
    line_chart.linechart(dailychart, axs[0])
    histogram2.histogram(n_20_plus, n_0_20_plus,n_0_20_minus, n_20_minus, axs[1])
    pie_chart.piechart(count_green_year, count_red_year, axs[2])
    
    plt.tight_layout()
    plt.show()
    user_prompt.runQuestion1()
    
        