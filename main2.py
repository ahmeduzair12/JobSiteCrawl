import scrapy
from scrapy.http import FormRequest
class QuotesSpider(scrapy.Spider):
    name = "quotes"
    page = 0

    def next_page(self):
        self.page = self.page + 1
        return FormRequest("https://www.monsterindia.com/jobsearch/searchresult.html",
            formdata={"ref": "https://www.monsterindia.com/job-search.html", "n": str(self.page), "srt": "pst"},
            callback=self.parse)

    def start_requests(self):
        return [ self.next_page() for x in range(0, 100)]
    def parse(self, response):
        for job in response.css('#hightlightedKeyword > div:nth-child(1) > div > ul.ullilist > li'):
            yield {
                'source': 'Monster',
                'position': job.css('div.row > div.col-sm-9 > div > div.jtitle > h2 > a > span::text').extract_first(),
                'company': job.css('div.row > div.col-sm-9 > div > div.jtxt.orange > a > span::text').extract_first(),
                'date': job.css('div.job_optwrap > div.job_optitem.ico7::text').extract_first(),
                'summary': job.css('div.row > div.col-sm-9 > div > div:nth-child(6) > span:nth-child(2)::text').extract_first(),
                'link':job.css('div.row > div.col-sm-9 > div > div.jtitle > h2 > a::attr(href)').extract_first()
            }

        # next_page = response.css('#hightlightedKeyword > div:nth-child(1) > div > ul.pager.pull-right > li:nth-child(2) > a::attr("href")').extract_first()
        # if next_page is not None:
        #     yield self.next_page()

