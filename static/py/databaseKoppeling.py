import pandas as pd
import sqlite3
import numpy as np
pd.options.display.max_columns = 20

def koppelDB():
    conn = sqlite3.connect('test.db')
    df2 = pd.read_sql_query("SELECT * FROM product3", conn)
    pk = "template_number" ## primary key waarop databases gekoppeld worden

    df2 = df2.dropna()
    del df2['id']
    del df2['barcode']
    del df2['datetime_created']
    print(df2)
    print()

    df1 = pd.read_csv("ResultsTemplateMatching.csv")
    template_names = list(df1[pk])
    template_names2 = list(df2[pk])

    template_names = [str(x) for x in template_names]   # Maakt alle templatenumbers into strings zodat
                                                        # beide kolommen strings zijn

    df2 = df2[df2[pk].isin(template_names)]
    df2[pk] = df2[pk].astype(str)
    df1[pk] = df1[pk].astype(str)


    print(df1)
    print()

    df = df1.merge(df2, how='inner', on=pk)
    print()
    print(df)

    df.to_sql(con=conn, if_exists="replace", name='match', index=False) # schrijf naar database

# koppelDB()

