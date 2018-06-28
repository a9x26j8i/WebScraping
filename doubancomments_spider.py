
"""
Created on Sat Apr 21 12:06:11 2018

@author: DELL
"""
from scrapy.spiders import Spider
from scrapy import Request
from mypy1.items import Mypy1Item
import re
#import requests
#import random

class DoubanMovieTop250Spider(Spider):
    name = "doubancomments"
    start_urls = ['https://movie.douban.com/top250']
    headers={}
    headers['User-Agent'] = "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.94 Safari/537.36"
    #TYPE1 for front page; TYPE2 for individual movies; TYPE3 for comment response
    TYPE = 1
        
    def start_requests(self):
        url = 'https://movie.douban.com/top250'
        r = Request(url, headers=self.headers)
#        r=requests.get(url,proxies={'http':random.choice(self.pro)},headers=self.headers)
        yield r
        
    def parse(self, response):   
        
        if response:        
            item = Mypy1Item()        
            #judgement of response type
            t = response.xpath('.//head/title/text()').extract()[0].strip()
            if t == '豆瓣电影 Top 250':
                self.TYPE = 1
            #individual movie page
            elif re.search(r'(豆瓣)',t)!=None :
                self.TYPE = 2
            #comment page
            else:
                self.TYPE = 3
                
                
            #for front pages
            if self.TYPE == 1:  
                movies = response.xpath('.//ol[@class="grid_view"]/li')
                #extract individual movie
                for movie in movies:
                    url = movie.xpath('.//div[@class="info"]//a[1]/@href').extract()[0] 
                    url = url + 'comments?status=P'
                    yield Request(url, headers=self.headers)  
                #extract next url of front page
                nexturl = 'https://movie.douban.com/top250' + response.xpath('.//span[@class="next"]/a/@href').extract()[0]
                yield Request(nexturl,headers=self.headers)
            #for comment page responses
            elif self.TYPE == 3:
                item = Mypy1Item()
                general = response.xpath('.//div[@id="content"]')
                movie = response.xpath('.//div[@class="mod-bd"]/div[@class="comment-item"]')
                
                for ci in movie:
        #            item['ranking'] = movie.xpath(
        #                './/div[@class="pic"]/em/text()').extract()[0] #discard[0]?引号？
        #            item['movie_name'] = movie.xpath(
        #                ".//div[@class='hd']/a/span[1]/text()").extract()[0]
        #            item['score'] = movie.xpath(
        #                ".//div[@class='star']/span[2]/text()").extract()[0]   #text()?
        #            item['score_num'] = movie.xpath(
        #                ".//div[@class='star']/span[4]/text()").re(r'(\d+)人评价')[0]
                    item['movie_name'] = general.xpath('./h1/text()').extract()[0]
                    item['comment'] = ci.xpath(
                    './/div[@class="comment"]/p/text()').extract()[0].strip()
                    item['user'] = ci.xpath(
                    ".//span[@class='comment-info']/a/text()").extract()[0]
                    yield item
                next_url = general.xpath('.//div[@class="aside"]/p/a/@href').extract()[0] + 'comments' + general.xpath('.//div[@id="paginator"]/a[@class="next"]/@href').extract()[0]
                
                yield Request(next_url, headers=self.headers)

                
            
            
            
            
            
            
