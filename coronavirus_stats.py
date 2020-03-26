import requests 
from bs4 import BeautifulSoup  
import os 
import numpy as np 
import matplotlib.pyplot as plt

extract_contents = lambda row: [x.text.replace('\n', '') for x in row] 
URL = 'https://www.mohfw.gov.in/'
  
heading = ['SNo', 'State','Indian-Confirmed', 
                 'Foreign-Confirmed','Cured','Death'] 
  
response = requests.get(URL).content 
soup = BeautifulSoup(response, 'html.parser') 
header = extract_contents(soup.tr.find_all('th')) 
  
stats = [] 
all_rows = soup.find_all('tr') 
  
for row in all_rows: 
    stat = extract_contents(row.find_all('td')) 
    if stat: 
        if len(stat) == 5: 
            # last row 
            stat = ['', *stat] 
            stats.append(stat) 
        elif len(stat) == 6: 
            stats.append(stat) 
  
stats[-1][1] = "Total Cases"
  
stats.remove(stats[-1]) 

objects = [] 
for row in stats : 
    objects.append(row[1])  
  
y_pos = np.arange(len(objects)) 
  
performance = [] 
for row in stats : 
    performance.append(int(row[2]) + int(row[3]))
table = stats
def print_table(table):
    longest_cols = [
        (max([len(str(row[i])) for row in table]) + 3)
        for i in range(len(table[0]))
    ]
    row_format = "".join(["{:>" + str(longest_col) + "}" for longest_col in longest_cols])
    for row in table:
        print(row_format.format(*row))
stats.insert(0,heading)
print_table(table)

plt.barh(y_pos, performance, align='center', alpha=0.5, 
                 color=(240/256.0, 128/256.0, 128/256.0), 
                 edgecolor=(0/256.0, 0/256.0, 0/256.0)) 
  
plt.yticks(y_pos, objects) 
plt.xlim(1,150) 
plt.xlabel('Number of Cases') 
plt.title('Corona Virus Cases') 
plt.show() 
