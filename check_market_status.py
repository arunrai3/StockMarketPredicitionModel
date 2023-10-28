import requests
import pulling_data


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