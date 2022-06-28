import pandas as pd
import sqlite3
import numpy as np
pd.options.display.max_columns = 20

conn = sqlite3.connect('test.db')
df2 = pd.read_sql_query("SELECT * FROM product3", conn)
# print(df2)
df2 = df2.dropna()
del df2['id']
del df2['barcode']
del df2['datetime_created']
# print(df2)
# print()

df1 = pd.read_csv("ResultsTemplateMatching.csv")
template_names = list(df1["template_number(RNG)"])
template_names2 = list(df2["template_number(RNG)"])

template_names = [str(x) for x in template_names]

df2 = df2[df2["template_number(RNG)"].isin(template_names)]
df2["template_number(RNG)"] = df2["template_number(RNG)"].astype(str)
df1["template_number(RNG)"] = df1["template_number(RNG)"].astype(str)
# print(df2)
# print(type(df2["product_name"]))



df = df1.merge(df2, how='inner', on="template_number(RNG)")
print()
print(df)

# df = df.dropna()
# del df["datetime_created"]
# print(df)
# df.to_csv("opgeslagen_dataframe",index=False)



