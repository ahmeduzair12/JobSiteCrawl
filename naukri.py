import scrapy
from scrapy.http import FormRequest
class QuotesSpider(scrapy.Spider):
    name = "quotes"
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
            yield {
                'source': 'Naukri',
                'position':  job.css('#jdUrl::text').extract_first(),
                'company': job.css('span.org::text').extract_first(),
                'summary': job.css('span.desc::text').extract_first(),
                'date': job.css('span.date::text').extract_first(),
                'link': job.css('#jdUrl::attr(href)').extract_first(),
                'Keyskills': job.css('span.skill::text').extract_first()
            }

        # next_page = response.css('#hightlightedKeyword > div:nth-child(1) > div > ul.pager.pull-right > li:nth-child(2) > a::attr("href")').extract_first()
        # if next_page is not None:
        #     yield self.next_page()

