from selenium import webdriver
import re
import csv
from datetime import datetime, timedelta
chrome_path = 'C:/bin/chromedriver.exe'
filename = 'job.csv'
job_file = open(filename, 'w')
# job_file = open(filename, 'w', encoding='utf-8')
job_file.close()

def get_next_button():
    return driver.find_element_by_css_selector('#hightlightedKeyword > div:nth-child(1) > div > ul.pager.pull-right > li:nth-child(2)')

def is_job_within(date):
    date_regex = r'(?<=[0-9])(?:st|nd|rd|th)'
    date = re.sub(date_regex, "", date)
    date_obj = datetime.strptime(date ,'%d %b %Y')
    return datetime.today() - timedelta(days=10) <= date_obj

job_data = []
job_data.append(['Source', 'url', 'role', 'date', 'description', 'Company Name'])
# job_data.append(job)
# [['Source', 'url', 'role', 'date', 'description'], ['Source', 'url', 'role', 'date', 'description'], ['Source', 'url', 'role', 'date', 'description']]
driver = webdriver.Chrome(executable_path=chrome_path)

driver.get('https://www.monsterindia.com/jobsearch/searchresult.html')
s_b_date = driver.find_element_by_css_selector('#hightlightedKeyword > div:nth-child(1) > div > div.result_head > div.relevance_freshness.pull-right > div > label.btn.btn-default:nth-child(2)')
s_b_date.click()

try:
    page = 0
    end_crawl = False
    while not end_crawl:
        # all_job_per_page = driver.find_elements_by_css_selector('#hightlightedKeyword > div:nth-child(1) > div > ul.ullilist > li')
        # Speed up code
        all_job_date = driver.find_elements_by_css_selector('#hightlightedKeyword > div:nth-child(1) > div > ul.ullilist > li div.job_optwrap > div.job_optitem.ico7')
        all_job_date = [x.text[9:] for x in all_job_date]
        data_range = len(all_job_date)
        for i in range(0, len(all_job_date)):
            if not is_job_within(all_job_date[i]):
                data_range = i - 1
                end_crawl = True
        # [dat1, dat2, dat3]
        all_job_heading_el = driver.find_elements_by_css_selector('#hightlightedKeyword > div:nth-child(1) > div > ul.ullilist > li div.row > div.col-sm-9 > div > div.jtitle > h2 > a')
        all_url = [x.get_attribute('href') for x in all_job_heading_el]
        all_job_role = [x.find_element_by_css_selector('span').text for x in all_job_heading_el]
        all_job_summary = driver.find_elements_by_css_selector('#hightlightedKeyword > div:nth-child(1) > div > ul.ullilist > li div.row > div.col-sm-9 > div > div:nth-child(6) > span:nth-child(2)')
        all_job_summary = [x.text for x in all_job_summary]
        all_job_company = driver.find_elements_by_css_selector('#hightlightedKeyword > div:nth-child(1) > div > ul.ullilist > li div.row > div.col-sm-9 > div > div.jtxt.orange > a > span')
        all_job_company = [x.text for x in all_job_company]
        # ['Monster', 'Monster', 'Monster']
        # End speed up code
        job_data = zip(['Monster' for x in range(0, data_range)], all_url[:data_range], all_job_role[:data_range], all_job_date[:data_range], all_job_summary[:data_range], all_job_company[:data_range])
        # current_job_data = ['Monster', job_url, job_role, job_date, job_summary, job_company]
        print('Appending jobs to file')
        job_file = open(filename, 'a', encoding='utf-8')
        #cv writing done here
        job_csv = csv.writer(job_file)
        print('Writing jobs line to file')
        job_csv.writerows(job_data)
        print('Clearing job buffer')
        job_data = []
        get_next_button().click()
        page = page + 1
        print('Fetching data from ' + str(page + 1))
except Exception as e:
    print(e)
finally:
    driver.close()
