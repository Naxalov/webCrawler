from scrapy import Request
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class CarSpider(CrawlSpider):
    name = 'car'
    allowed_domains = ["www.olx.uz"]

    start_urls = [
        # 'http://quotes.toscrape.com/page/1/',

        'https://www.olx.uz/oz/transport/legkovye-avtomobili/chevrolet/'
    ]

    # rules = (
    #     Rule(LinkExtractor(allow=(), restrict_css=('span.fbold.next a::attr(href)',)),
    #          callback="parse_item",
    #          follow=True),)

    def parse(self, response):
        # page = response.url
        print('Processing..' + response.url)
        next_page = response.css('span.fbold.next a::attr(href)').get()
        links = response.css('.link.detailsLink::attr(href)').extract()
        for a in links:
            yield Request(a, callback=self.parse_detail_page)

        print('next:{}'.format(next_page))

        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield Request(next_page, callback=self.parse)

    def parse_detail_page(self, response):
        images = response.css('.vtop.bigImage::attr(src)').extract()

        yield {'images': images,}
