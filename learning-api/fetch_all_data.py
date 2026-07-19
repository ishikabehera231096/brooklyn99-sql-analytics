import pandas as pd
import requests
import time
import json

import os

if os.path.exists("omdb_raw_cache.json"):
       print("Cache found — loading from disk instead of calling the API")
       with open("omdb_raw_cache.json", "r") as f:
           all_results = json.load(f)
else:
       print("No cache found — fetching from OMDb API")

df = pd.read_csv("/Users/ishik/Desktop/brooklyn99-sql-analytics/exports/b99_episodes_cleaned.csv")
episode_list = df[["Season", "Episode"]].to_dict("records")


api_key = "a0dcb515"
url = "http://www.omdbapi.com/"
all_results = []

for ep in episode_list:
       params = {
           "apikey": api_key,
           "t": "Brooklyn Nine-Nine",
           "Season": ep["Season"],
           "Episode": ep["Episode"]
       }

       response = requests.get(url, params=params)
       data = response.json()

       if data.get("Response") == "True":
           all_results.append(data)
       else:
           print(f"Failed: Season {ep['Season']} Episode {ep['Episode']} - {data.get('Error')}")

       time.sleep(0.5)



with open("omdb_raw_results.json", "w") as f:
    json.dump(all_results, f, indent=2)

print("Saved results to omdb_raw_results.json")