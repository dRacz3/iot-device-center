import pandas, pandas_bokeh
pandas_bokeh.output_file("temp.html")


import sqlite3
import pandas as pd
# Create your connection.
cnx = sqlite3.connect('database.db')


df = pd.read_sql_query("SELECT * FROM MEASUREMENTS", cnx)
df[df['VALUE'] < df['VALUE'].max() * 0.95]

df['TIME'] = pandas.to_datetime(df['TIME'], unit = 's')
df.set_index("TIME").rolling(window = int(60/5)).mean().plot_bokeh()