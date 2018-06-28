import scrapy
from ..items import WikiItem

class WikiEntrySpider(scrapy.Spider):

#    name = 'baidubaike'
#    count = 1
#    
#    headers  = {
#                'User-Agent':{'User-Agent': 'User-Agent:Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0;'},
#                }
#    def start_request(self):
#        urls = ['http://www.baidu.com']
#        for url in urls:
#            yield scrapy.Request(url, headers = self.headers, callback = self.parse_frontpage)

               
    name = "baidubaike"
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
               }
    count = 1
    def start_requests(self):
        '''enter the front page'''
        url = ['https://baike.baidu.com/item/%E7%9F%A5%E4%B9%8E', 'https://baike.baidu.com/item/%E9%9F%A9%E6%9C%9D%E9%A6%96%E8%84%91%E7%AC%AC%E4%B8%89%E6%AC%A1%E4%BC%9A%E6%99%A4',]
        for u in url:
            yield scrapy.Request(u, headers=self.headers)

            
    def parse(self, response):
        if self.count <= 10000:
            print("=============================")
            urls = response.xpath('//div[@class="main-content"]/div[@class="lemma-summary"]//a/@href').extract()
            item = WikiItem()
            for url in urls:
                aburl = response.urljoin(url)
                yield scrapy.Request(aburl, headers = self.headers)
                
            title = response.xpath('//div[@class="main-content"]/dl/dd/h1/text()').extract()[0].strip()
            content = response.xpath('//div[@class ="main-content"]/div[@class="lemma-summary"]')
            content = content.xpath('string(.)').extract()[0].strip()
            
#            pattern = r'{"pv":(.*?)}'
#            volumes = re.search(pattern, response.text)
#            print('parse finished----------------------')
#            print(volumes[0])
            item['title'] = title
            item['content'] = content
            self.count += 1

            yield item
        else:
            return
        
        
        
        