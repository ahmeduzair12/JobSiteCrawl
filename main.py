import json
import xlsxwriter
import re
from datetime import datetime, timedelta

import scrapy
from scrapy import FormRequest
from scrapy.crawler import CrawlerProcess

naukri_data = []
monster_data = []
class MonsterSpider(scrapy.Spider):
    name = "Monster"
    page = 0

    def next_page(self):
        self.page = self.page + 1
        return FormRequest("https://www.monsterindia.com/jobsearch/searchresult.html",
            formdata={"ref": "https://www.monsterindia.com/job-search.html", "n": str(self.page), "srt": "pst"},
            callback=self.parse)

    def start_requests(self):
        return [ self.next_page() for x in range(0, 1000)]
    def parse(self, response):
        for job in response.css('#hightlightedKeyword > div:nth-child(1) > div > ul.ullilist > li'):
            t = {
                'source': 'Monster',
                'position': job.css('div.row > div.col-sm-9 > div > div.jtitle > h2 > a > span::text').extract_first(),
                'company': job.css('div.row > div.col-sm-9 > div > div.jtxt.orange > a > span::text').extract_first(),
                'date': job.css('div.job_optwrap > div.job_optitem.ico7::text').extract_first(),
                'summary': job.css('div.row > div.col-sm-9 > div > div:nth-child(6) > span:nth-child(2)::text').extract_first(),
                'link':job.css('div.row > div.col-sm-9 > div > div.jtitle > h2 > a::attr(href)').extract_first(),
                'Keyskills':job.css('div.row > div.col-sm-9 > div > div:nth-child(5) > span:nth-child(2)::text').extract_first()
            }
            monster_data.append(t)

class NaukriSpider(scrapy.Spider):
    name = "Naukri"
    page = 0

    def next_page(self):
        self.page = self.page + 1
        url = 'https://www.naukri.com/jobs-in-india-' + str(self.page)
        return FormRequest(url,
            formdata={"qs": "f", "qco[]": "10"},
            callback=self.parse)

    def start_requests(self):
        return [ self.next_page() for x in range(0, 1000)]
    def parse(self, response):
        for job in response.css('body > div.mainSec > div > div.container.fl > div.srp_container.fl > div[type="tuple"]'):
            t = {
                'source': 'Naukri',
                'position':  job.css('#jdUrl::text').extract_first(),
                'company': job.css('span.org::text').extract_first(),
                'summary': job.css('span.desc::text').extract_first(),
                'date': job.css('span.date::text').extract_first(),
                'link': job.css('#jdUrl::attr(href)').extract_first(),
                'Keyskills': job.css('span.skill::text').extract_first()
            }
            naukri_data.append(t)

process = CrawlerProcess()
process.crawl(NaukriSpider)
process.crawl(MonsterSpider)
process.start()

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
json_data = monster_data
#creating an array
xls_data = []
#loading the json file data of monster
for i in json_data:
    if is_job_within_monster(i['date'][9:]):
        # xls_data.append([i['company'], i['summary'], i['source'], i['link'], i['date'][9:], i['position'],i['Keyskills']])
        xls_data.append([i['source'], i['date'][9:], i['company'], 'https:' +i['link'], i['position'], i['Keyskills'],i['summary']])
#loading the json of naukri
json_data = naukri_data
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