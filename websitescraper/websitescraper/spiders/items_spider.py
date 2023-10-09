import scrapy
from websitescraper.items import ScraperItem


class ItemsSpiderSpider(scrapy.Spider):
    name = "items_spider"
    allowed_domains = ["douglas.de"]
    start_urls = ["https://www.douglas.de/de/c/parfum/unisex-duefte/0103"]

    def parse(self, response):
        items = response.css('div[class*="product-grid-column"] > div')
        for item in items:
            scrap_item = ScraperItem()
            scrap_item['name'] = item.css('div[class="text name"]::text').get(),
            scrap_item['brand'] = item.css('div[class="text top-brand"]::text').get(),
            scrap_item['price'] = item.css('span[class="product-price__price"]::text').get(),
            scrap_item['category'] = item.css('div[class="text category"]::text').get(),
            scrap_item['volume'] = item.css('span.product-price__extended-content-units::text').get(),
            scrap_item['rating'] = item.css('span[data-testid="rating-stars"]::attr(data-average-rating)').get()
            yield scrap_item

        # next_page = response.css('a[data-testid="pagination-arrow-right"]::attr(href)').get()
        # if next_page:
        #     next_page_url = 'https://www.douglas.de' + next_page
        #     yield response.follow(next_page_url, callback=self.parse)
