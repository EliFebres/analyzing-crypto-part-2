import re
import json
import pandas as pd
import numpy as np


f = open('Data.txt', 'r')
data = f.read()

# Change All Coin Numbers to Coin Names
data1 = data.replace('''"1"''', '''"Bitcoin"''')
data2 = data1.replace('''"52"''', '''"XRP"''')
data3 = data2.replace('''"825"''', '''"Tether"''')
data4 = data3.replace('''"1027"''', '''"Ethereum"''')
data5 = data4.replace('''"1839"''', '''"BNB"''')
data6 = data5.replace('''"2010"''', '''"Cardano"''')
data7 = data6.replace('''"3408"''', '''"USD Coin"''')
data8 = data7.replace('''"4172"''', '''"Terra"''')
data9 = data8.replace('''"5426"''', '''"Solana"''')
data10 = data9.replace('''"6636"''', '''"Polkadot"''')
data11 = data10.replace('''"other_total_market_cap"''', '''"Other"''')
data12 = data11.replace('''"global"''', '''"Total"''')

# Get rid of everything in between lists
stripped = re.sub('\d\d\d\d-\d\d-\d\d\w\d\d:\d\d:\d\d\.\d\d\d\w',"",data12)
stripped2 = stripped.replace(''',"":''', ';')
# print(stripped2)

#spit out a list of each dictionary
listed_stripped = stripped2.split(";")

list_of_dicts = []
for i in range(len(listed_stripped)):
    res = json.loads(listed_stripped[i])
    list_of_dicts.append(res)

fut_data = pd.DataFrame(list_of_dicts)
print(fut_data)

fut_data.to_excel("output.xlsx")