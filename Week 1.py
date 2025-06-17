import pandas as pd
import altair as alt

data = pd.read_csv('../Data/WHR_2016.csv')
data.head()

alt.Chart(data).mark_bar().encode(
    x = "Region",
    y = "Happiness Rank"
)


strs = ["ab", "a"]

result = ''
temp = ''
for i in strs:
    if len(i) == 0:
        result = ''
        break
    if result == '':
        result = i
        continue
    if i[0] != result[0]:
        result = ''
        break
    for j in range(min(len(i)-1, len(result)-1)):
        if i[j] == result[j]:
            temp = temp + i[j]
    result = temp
    temp = ''
