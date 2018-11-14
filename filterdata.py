import json
import xlsxwriter
import re
from datetime import datetime, timedelta
import os

# running scrapy files on terminal
# os.system('del monster.json | naukri.json')
# os.system("scrapy runspider .\naukri.py -o naukri.json")
# os.system("scrapy runspider .\monster.py -o monster.json;scrapy runspider .\naukri.py -o naukri.json")
# os.system("")

f_json = open('monster.json', 'r', encoding='utf-8')
n_json = open('naukri.json', 'r', encoding='utf-8')

def is_job_within_monster(date):
    date_regex = r'(?<=[0-9])(?:st|nd|rd|th)'
    date = re.sub(date_regex, "", date)
    date_obj = datetime.strptime(date ,'%d %b %Y')
    return datetime.today() - timedelta(days=10) <= date_obj

def is_n_days_ago(date):
    date1 = str(date)
    regexmatch = re.search('([0-9]+)',date1,re.IGNORECASE)
    if not regexmatch:
        return True
    count = regexmatch.group(1)
    return int(count)<=10

#loading the json file data of monster
json_data = json.load(f_json)
#creating an array
xls_data = []
#loading the json file data of monster
for i in json_data:
    if is_job_within_monster(i['date'][9:]):
        # xls_data.append([i['company'], i['summary'], i['source'], i['link'], i['date'][9:], i['position'],i['Keyskills']])
        xls_data.append([i['source'], i['date'][9:], i['company'], i['link'], i['position'], i['Keyskills'],i['summary']])
#loading the json of naukri
json_data = json.load(n_json)
for i in json_data:
    # xls_data.append([i['company'], i['summary'], i['source'], i['link'], i['date'], i['position'],i['Keyskills']])
    if is_n_days_ago(i['date']):
        xls_data.append([i['source'], i['date'], i['company'], i['link'], i['position'], i['Keyskills'],i['summary']])

workbook = xlsxwriter.Workbook('jobs.xlsx')
worksheet = workbook.add_worksheet()
worksheet.write('A1', 'Source')
worksheet.write('B1', 'Date')
worksheet.write('C1', 'Company')
worksheet.write('D1', 'Link')
worksheet.write('E1', 'Position')
worksheet.write('F1', 'Keyskills')
worksheet.write('G1', 'Summary')
row = 1
col = 0

for item in xls_data:
    worksheet.write_string(row, col,     item[0] or "")
    worksheet.write_string(row, col + 1, item[1] or "")
    worksheet.write_string(row, col + 2, item[2] or "")
    worksheet.write_string(row, col + 3, item[3] or "")
    worksheet.write_string(row, col + 4, item[4] or "")
    worksheet.write_string(row, col + 5, item[5] or "")
    worksheet.write_string(row, col + 6, item[6] or "")
    row += 1

workbook.close()