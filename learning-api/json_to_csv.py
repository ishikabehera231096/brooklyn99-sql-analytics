import pandas as pd
import json

with open("omdb_raw_results.json", "r") as f:
    all_results = json.load(f)

df_omdb = pd.DataFrame(all_results)
df_omdb.to_csv("/Users/ishik/Desktop/brooklyn99-sql-analytics/data/omdb_raw.csv", index=False)