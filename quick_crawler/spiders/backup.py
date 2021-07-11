import scrapy
from ..items import QuickCrawlerItem


class QuoteSpider(scrapy.Spider):
    name = 'quotes'
    page_number = 2
    start_urls = [
        'https://quotes.toscrape.com/page/1/'
    ]

    def parse(self, response):
        # title = response.css('title::text').extract()
        # yield {'titletext':title}

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

        next_page = 'https://quotes.toscrape.com/page/'+str(QuoteSpider.page_number)+'/'
        if QuoteSpider.page_number <= 11:
            QuoteSpider.page_number += 1
            yield response.follow(next_page, callback = self.parse)
