import scrapy


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = [
        'https://www.monsterindia.com/jobsearch/searchresult.html',
    ]

    def parse(self, response):
        for quote in response.css('#hightlightedKeyword > div:nth-child(1) > div > ul.ullilist > li'):
            yield {
                'position': quote.css('div.row > div.col-sm-9 > div > div.jtitle > h2 > a > span::text').extract_first(),
                'company': quote.css('div.row > div.col-sm-9 > div > div.jtxt.orange > a > span::text').extract_first(),
                'date': quote.css('div.row > div.col-sm-9 > div > div.jtxt.orange > a > span::text').extract_first()
            }

        next_page = response.css('#hightlightedKeyword > div:nth-child(1) > div > ul.pager.pull-right > li:nth-child(2) > a::attr("href")').extract_first()
        if next_page is not None:
            yield response.follow(next_page, self.parse)
