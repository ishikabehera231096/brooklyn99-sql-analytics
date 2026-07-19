import requests

API_KEY = "a0dcb515"
url = "http://www.omdbapi.com/"
params = {
       "apikey": API_KEY,
       "t": "Brooklyn Nine-Nine",
       "Season": 1,
       "Episode": 1
   }
response = requests.get(url, params=params)
print(response.json())