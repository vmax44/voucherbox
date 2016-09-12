    # -*- coding: utf-8 -*-
import scrapy
import json
from urllib.parse import urljoin


class VoucherboxSpider(scrapy.Spider):
    name = "voucherbox"
    allowed_domains = ["voucherbox.co.uk"]
    api_url='https://www.voucherbox.co.uk/ajax/lazy-load-vouchers'
    start_urls=['https://www.voucherbox.co.uk/categories']
    categories=[]
    file_number=1



    def construct_request(self,page,category):
        req=scrapy.FormRequest(self.api_url,
                                   formdata={'start':page, 'category_alias':category},
                                   callback=self.parse_category)
        req.meta['category']=category
        return req

    def parse_categories(self,response):
        s=scrapy.Selector(response)
        cats=s.css('a.wg-categorylist_anchor::attr(href)').extract()
        self.categories=[c[1:] for c in cats]

    def parse(self, response):
        self.parse_categories(response)
        for category in self.categories:
            yield self.construct_request('1',category)

    def parse_category(self, response):
        j = json.loads(response.body.decode("utf-8"))
        for item_url in self.parse_items_urls(j['view'],response,response.url):
            yield item_url
        if j['remaining']>0 and j['start']<=1:
            yield self.construct_request(str(j['start']),response.meta['category'])

    def parse_items_urls(self, html, response, baseurl):
        cel=scrapy.Selector(text=html)
        for a in set(cel.css('a.wg-discount_shop-link_anchor::attr(href)').extract()):
            req=scrapy.Request(urljoin(baseurl,a),callback=self.parse_item)
            req.meta['category']=response.meta['category']
            yield req

    def parse_item(self, response):
        #self.save_to_file(response)
        c=scrapy.Selector(response)
        data=c.css("script[type='application/ld+json']::text").extract_first("").strip()
        i=dict()
        if data:
            j=json.loads(data)
            i['category']=response.meta['category']
            i['url']=j.get('url','')
            i['name']=j.get('name','')
            i['logo']=j.get('logo','')
            i['description']=j.get('description','')
        else:
            self.logger.error('Error parsing item %s' % response.url)
            i['category']=response.meta['category']
            i['url']=response.url
            i['name']=''
            i['logo']=''
            i['description']='error'
        yield i

    def save_to_file(self,response):
        filename=response.url.split("/")[-1]
        with open(filename+".html",'w') as f:
            print(response.body, file=f)