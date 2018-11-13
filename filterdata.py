import json, csv


f_csv = open('jobs.csv', 'w', encoding='utf-8')
f_json = open('quotes.json', 'r', encoding='utf-8')
n_json = open('naukri.json', 'r', encoding='utf-8')
json_data = json.load(f_json)
csv_data = []
for i in json_data:
    csv_data.append([i['company'], i['summary'], i['source'], i['link'], i['date'], i['position']])
json_data = json.load(n_json)

for i in json_data:
    csv_data.append([i['company'], i['summary'], i['source'], i['link'], i['date'], i['position']])

a = csv.writer(f_csv)
a.writerows(csv_data)
