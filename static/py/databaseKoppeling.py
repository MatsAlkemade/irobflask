import pandas as pd
import sqlite3
import numpy as np
pd.options.display.max_columns = 20

conn = sqlite3.connect('test.db')

df = pd.read_sql_query("SELECT * FROM product", conn)

print(df)

df.to_sql("product2", conn, if_exists='replace', index=False)








# df1 = pd.read_csv(r"ResultsTemplateMatching.csv")
# df2 = pd.read_csv(r"barcode_test.csv")
#
# df = df1.join(df2, lsuffix="_results", rsuffix="_barcodes")
# cols = df.columns.tolist()
# print(df)
# print(cols)
# # print(df)
# df = df[["primary_key","barcode_value","product_name","accuracy_score", "template_name", "datetime_results"]]
# df = df.dropna()
# df["primary_key"] = df["primary_key"].astype(int)
#
# print(df)
# df.to_csv("opgeslagen_dataframe",index=False)



