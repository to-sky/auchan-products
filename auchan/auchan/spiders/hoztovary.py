# -*- coding: utf-8 -*-
import json
import re
import scrapy
from auchan.items import AuchanItem


class HoztovarySpider(scrapy.Spider):
    name = 'hoztovary'
    allowed_domains = ['auchan.ru']
    start_urls = ['https://www.auchan.ru']

    # def start_requests(self):
    #     urls = [
    #         'https://www.auchan.ru/pokupki/sms-2400g-aistenok.html'
    #     ]
    #     for url in urls:
    #        yield scrapy.Request(url=url, callback=self.item)

    def parse(self, response):
        menu_items = response.css('.topnav__menu .m-menu__items > li')

        for item in menu_items:
            all_category_link = item.css('.m-menu__title a::attr(href)').extract_first()

            if all_category_link == 'https://www.auchan.ru/pokupki/hoztovary.html':
                hoztovary_categories = item.css('.m-menu__submenu-col .m-menu__submenu-block')

                for link in hoztovary_categories:
                    link_item = link.css('.m-menu__submenu-item-link')

                    if link_item:
                        url = link.css('.m-menu__submenu-item-link::attr(href)').extract_first()
                        yield response.follow(url, self.category)

    def category(self, response):
        # 43 - id of first { in json variable productListBlockJson
        data_json = re.findall('productListBlockJson.*= {.*};', response.text)[0][43:-1]
        data = json.decoder.JSONDecoder().decode(data_json)
        for product in data['products']:
            yield scrapy.Request(product['url'], self.item)

        pager = data['toolbarInitData']['pagerInitData']
        if not pager['currentPage'] == pager['lastPage']:
            for page in pager['pages']:
                if pager['currentPage'] + 1 == page['num']:
                    yield scrapy.Request(page['url'], self.category)

    def item(self, response):
        # Exclude 'Каждый день' brand
        brand = response.xpath("//span[contains(text(), 'Бренд')]/following-sibling::strong/text()").extract_first()
        if brand == 'Каждый день' or brand == 'Auchan':
            return

        item = AuchanItem()
        item['name'] = response.css('.prcard__title h1::text').extract_first()
        item['price'] = response.css('.prcard__price-block .price-val::text').extract_first().replace(',', '')
        item['image_url'] = response.css('.prcard__details meta[itemprop=image]::attr("content")').extract_first()
        item['categories'] = response.css('.breadcrumbs__list li')[2:].css('span::text').extract()
        item['description'] = self.get_description
        item['sku'] = response.xpath("//span[contains(text(), 'Артикул')]/following-sibling::strong/text()").extract_first()

        # Get all attributes
        attrs = {}
        for attr in response.css('.prcard__feat-list li'):
            attr_name = attr.css('span::text').extract_first()[:-1]
            attr_value = attr.css('strong::text').extract_first()

            if attr_name != 'Артикул':
                attrs.update({
                    attr_name: attr_value
                })

        item['attributes'] = json.dumps(attrs, ensure_ascii=False).encode('utf8')
        yield item

    def get_description(self, response):
        desc_dirty = response.css('.prcard__desc-txt p::text').extract()
        desc_clear = list(filter(lambda x: x != '\xa0', desc_dirty))
        description = '\n'.join(desc_clear)

        return description
