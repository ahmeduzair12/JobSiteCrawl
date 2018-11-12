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
        all_job_per_page = driver.find_elements_by_css_selector('#hightlightedKeyword > div:nth-child(1) > div > ul.ullilist > li')
        # Speed up code
        # all_job_date = driver.find_elements_by_css_selector('#hightlightedKeyword > div:nth-child(1) > div > ul.ullilist > li div.job_optwrap > div.job_optitem.ico7')
        # some code
        job_count = 1
        for i in range(0, len(all_job_per_page)):
            # process each data 
            job_element = all_job_per_page[i]
            job_date = job_element.find_element_by_css_selector('div.job_optwrap > div.job_optitem.ico7').text[9:]
            # Compare the date if it is within 10 days
            if not is_job_within(job_date):
                end_crawl = True
                break
            # if it is collect other data
            job_heading_el = job_url = job_role = ''
            try:
                job_heading_el = job_element.find_element_by_css_selector('div.row > div.col-sm-9 > div > div.jtitle > h2 > a')
            except Exception as e:
                print('Error in heading')
                print(e)
            try:
                job_url = job_heading_el.get_attribute('href')
            except Exception as e:
                print('Error in URL')
                print(e)
            try: 
                job_role = job_heading_el.find_element_by_css_selector('span').text
            except Exception as e:
                print('Error in job role')
                print(e)
            except Exception as e:
                print(e)
            job_summary = ''
            try:
                job_summary = job_element.find_element_by_css_selector('div.row > div.col-sm-9 > div > div:nth-child(6) > span:nth-child(2)').text
            except Exception as e:
                job_summary = 'No Summary'
            job_company = ''
            try:
                job_company = job_element.find_element_by_css_selector('div.row > div.col-sm-9 > div > div.jtxt.orange > a > span').text
            except Exception as e:
                job_company = 'No Summary'
            # finally append the row data
            # current_job_data = ['Monster', job_url, job_role.encode("utf-8"), job_date.encode("utf-8"), job_summary.encode("utf-8"), job_company.encode("utf-8")]
            current_job_data = ['Monster', job_url, job_role, job_date, job_summary, job_company]
            # current_job_data = ['Monster', job_url.encode("utf-8").decode("utf-8"), job_role.encode("utf-8").decode("utf-8"), job_date.encode("utf-8").decode("utf-8"), job_summary.encode("utf-8").decode("utf-8"), job_company.encode("utf-8").decode("utf-8")]
            # print(current_job_data)
            job_data.append(current_job_data)
            print('Job ' + str(job_count))
            job_count = job_count + 1
        # add_data_to_file()
        # job_data = 0
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
