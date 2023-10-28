import sys
import pulling_data
import quant_analysis

def runQuestion1():
    answer = input("\n\nEnter stock to view analysis for. Please type the ticker symbol for stock in CAPS, Only availabe stocks currently are(TSLA,AMZN,NFLX,MSFT,AAPL,GOOG). Or type \"q\" to quit.\n\n>")
    if answer == "TSLA" or answer == "NFLX" or answer == "AMZN" or answer == "MSFT" or answer == "AAPL" or answer == "GOOG":
        runQuestion2(answer)
    elif answer == "q":
        print("Program ended.")
        sys.exit()
    else:
        print("\n\nIm sorry I dont think I understood that. Please try and answer again.    NOTE: Answers are case sensitive.")
        runQuestion1()

def runQuestion2(stock):
    answer = input("\n\nSelect what type of analysis you would like to peform on " + stock + "? Please choose one of the options below by typing the letter next to that option. Case sensitive\n\na - Prediction model using AI/ML\nb - Quantitave Analysis\nr - Return to Main Menu\n\n>")
    if answer == "a":
        pulling_data.predicitionModelDataPull(stock)
    elif answer == "b":
        quant_analysis.quantAnalysis(stock)
    elif answer == "r":
        runQuestion1()
    else:
        print("\n\nIm sorry I dont think I understood that. Please try and answer again.    NOTE: Answers are case sensitive.")
        runQuestion2(stock)
