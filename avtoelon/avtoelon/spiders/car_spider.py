from scrapy import Request
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class CarSpider(CrawlSpider):
    name = 'car'
    # allowed_domains = ["www.avtoelon.uz"]

    start_urls = [
        # 'http://quotes.toscrape.com/page/1/',

        'https://avtoelon.uz/avto/chevrolet/'
    ]

    # rules = (
    #     Rule(LinkExtractor(allow=(), restrict_css=('span.fbold.next a::attr(href)',)),
    #          callback="parse_item",
    #          follow=True),)

    def parse(self, response):
        # page = response.url
        next_page = response.css('.pag-next-page a::attr(href)').get()
        links = response.css('.row.list-item>a::attr(href)').extract()
        for url in links:
            url = response.urljoin(url)
            # url = 'https://avtoelon.uz/avto/chevrolet' + url
            yield Request(url, callback=self.parse_detail_page)

        if next_page is not None:
            next_page = response.urljoin(next_page)
            print('next: {}'.format(next_page))
            yield Request(next_page, callback=self.parse)
        #
        # print('Processing..' + response.url)

    def parse_detail_page(self, response):
        title_text = response.css('title::text').get()
        img = response.css('.small-thumb::attr(href)').extract()

        yield {
            'title': title_text,
            'images': img
        }
