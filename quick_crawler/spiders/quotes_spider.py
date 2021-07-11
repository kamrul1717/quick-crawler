import scrapy
from scrapy.http import FormRequest
from scrapy.utils.response import open_in_browser
from ..items import QuickCrawlerItem


class QuoteSpider(scrapy.Spider):
    name = 'quotes'
    start_urls = [
        'https://quotes.toscrape.com/login'
    ]

    def parse(self, response):
        token = response.css("form input::attr(value)").extract_first()
        return FormRequest.from_response(response, formdata = {
            'csrf_token': token,
            'username': 'test',
            'password': 'test'
        }, callback = self.start_scraping)

    def parsePaginationData(self, response):
        items = QuickCrawlerItem()
        all_div_quotes = response.css("div.quote")
        for quote in all_div_quotes:
            title = quote.css('span.text::text').extract()
            author = quote.css('.author::text').extract()
            tag = quote.css('.tag::text').extract()
            items['title'] = title
            items['author'] = author
            items['tag'] = tag
            yield items

    def start_scraping(self, response):
        open_in_browser(response)
        items = QuickCrawlerItem()
        all_div_quotes = response.css("div.quote")
        page_number = 2
        for quote in all_div_quotes:
            title = quote.css('span.text::text').extract()
            author = quote.css('.author::text').extract()
            tag = quote.css('.tag::text').extract()
            items['title'] = title
            items['author'] = author
            items['tag'] = tag
            yield items

            next_page = 'https://quotes.toscrape.com/page/' + str(page_number) + '/'
            if page_number <= 11:
                page_number += 1
                yield response.follow(next_page, callback=self.parsePaginationData)

