# -*- coding: utf-8 -*-
"""
Created on Sat Apr 21 19:32:39 2018

@author: DELL
"""
from scrapy import Request
from scrapy.spiders import Spider
from mypy1.items import Mypy1Item

import json
import re

class DoubanActionSpider(Spider):
    name = 'douban_ajax'
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',    
    }
    count = 0
    
    def start_requests(self):
        url = 'https://movie.douban.com/j/chart/top_list?type=5&interval_id=100%3A90&action=&start=0&limit=20'
        yield Request(url, headers = self.headers)
        
    def parse(self,response):
        item = Mypy1Item()
        datas = json.loads(response.body.decode('utf-8'))
        
        if self.count<2:
            for data in datas:
                item['ranking'] = data['rank']
                item['score'] = data['score'] #rating?
                item['movie_name'] = data['title']
                item['score_num'] = data['vote_count']
                yield item
            
            page_num = re.search(r'start=(\d+)', response.url).group(1) #group(1)?
            page_num = 'start=' + str(int(page_num)+20)
            next_url = re.sub(r'start=\d+', page_num, response.url)
            yield Request(next_url, headers = self.headers)
            self.count += 1

            
                
                
                
