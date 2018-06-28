# -*- coding: utf-8 -*-
import scrapy
from ..items import SingerInfoItem
import webbrowser

class Singerinfo_Spider(scrapy.Spider):
    '''spider for info of netease music singer '''
    name = "singerinfo"
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
               'Cookie': '_iuqxldmzr_=32; _ntes_nnid=1155203d15f6df501f3765c0485f7b16,1524062836058; _ntes_nuid=1155203d15f6df501f3765c0485f7b16; WM_TID=vLqDIQXuCjPbbTVY3dxDIaZY596LWG9F; __remember_me=true; __f_=1525025598419; __utmc=94650624; __utmz=94650624.1525236473.25.6.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __utma=94650624.964334915.1524062840.1525236473.1525241150.26; MUSIC_U=e3e7809fdb6e12489911d1e1b7697133c00102734abd7dce5a46b50fd60f8d28add53ac92be248e0c4b635d5f08e00d131b299d667364ed3; __csrf=301aaf34542cc8e08272ee30d240263a; __utmb=94650624.4.10.1525241150; JSESSIONID-WYYY=ZtKQikjjIqiAB8K5deA9B8Rk80reIIksy0arCUUOCiId6ZTJHXq0HltM%2BOmn58pISmi4HF6jFrVn0y%5CWEjug%2B38usgxSix0kGZte3B55%2FBlHWDiV%5C4%5CrwQGGwZZbqYTSfbQb6vErSDhSMjD3oF3pfB7Sfzo992VcDxoAXtJe705Q1CFf%3A1525243495909',
               'Host': 'music.163.com',
               'Referer': 'http://music.163.com/',
               }
    
    def start_requests(self):
        '''enter the front page'''
        url = ['https://music.163.com/',]
        for u in url:
            yield scrapy.Request(u, headers=self.headers, callback=self.parse_frontpage) 

    def parse_frontpage(self, response):
        '''enter singer page'''
        url = response.xpath("//ul[@class='nav']/li[5]/a/@href").extract()[0]
        url = response.urljoin(url)
        yield scrapy.Request(url, headers=self.headers, callback=self.parse_category)
    
    def parse_category(self, response):
        '''extract urls of singer lists classfied by rigions'''
        url = response.xpath("//ul[@class='nav f-cb']/li/a[not(contains(text(),'推荐') or contains(text(),'入驻'))]/@href").extract()
        for u in url:
            url = response.urljoin(u)
            yield scrapy.Request(url, headers=self.headers, callback=self.parse_singerlist)
    
    def parse_singerlist(self, response):
        '''extract urls of singer lists from A to Z&others'''
        url = response.xpath("//ul[@class='n-ltlst f-cb']/li/a[not(contains(text(),'热门')) or contains(text(),'其他')]/@href").extract()
        for u in url:
            url = response.urljoin(u)
            yield scrapy.Request(url, headers=self.headers, callback=self.parse_singerpage)
    
    def parse_singerpage(self, response):
        '''extract individual singer urls'''
        url = response.xpath("//ul[@class='m-cvrlst m-cvrlst-5 f-cb']/li/p/a[1]/@href").extract()
        url.extend(response.xpath("//ul[@id='m-artist-box']/li/a[1]/@href").extract())
        for u in url:
            url=response.urljoin(u)
            yield scrapy.Request(url, headers=self.headers, callback=self.parse_info)
     
    def parse_info(self, response):
        '''extract info from singer pages'''
        songs = response.xpath("//ul[@class='f-hide']/li/a/text()").extract()
        singer = response.xpath("//h2[@id='artist-name']/text()").extract()[0]
        #intro = response.xpath("//meta[@name='description']/@content").extract()[0]
        '''save items'''
        item = SingerInfoItem()
        for song in songs:
            item['singer']= singer
            item['url'] = response.url
 #           item['intro'] = 
            item['song'] = song
            yield item
            
            
            
            
            