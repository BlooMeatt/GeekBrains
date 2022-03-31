import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem


class LabirintSpider(scrapy.Spider):
    name = 'labirint'
    allowed_domains = ['labirint.ru']
    start_urls = ['https://www.labirint.ru/genres/2684/']

    def parse(self, response: HtmlResponse):
        next_page = response.xpath("//a[@class = 'pagination-next__text']/@href").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        links = response.xpath("//a[@class = 'product-title-link']/@href").getall()
        for link in links:
            yield response.follow(link, callback=self.books_parse)

    def books_parse(self, response: HtmlResponse):
        name = response.xpath('//div[@id="product-title"]/h1/text()').get()
        author = response.xpath('//*[@id="product-specs"]/div[1]/div[2]/a/text()').get()
        price = response.xpath('//span[@class="buying-price-val-number"]/text()').get()
        if price is None:
            price_old = response.xpath('//span[@class="buying-priceold-val-number"]/text()').get()
            price_new = response.xpath('//span[@class="buying-pricenew-val-number"]/text()').get()
        else:
            price_old = None
            price_new = None
        rating = response.xpath('//*[@id="rate"]/text()').get()
        url = response.url
        book_id = response.xpath('//div[@class="articul"]/text()').get()
        yield JobparserItem(name=name, author=author, price=price, price_new=price_new, price_old=price_old,
                            rating=rating, url=url, _id=book_id)
