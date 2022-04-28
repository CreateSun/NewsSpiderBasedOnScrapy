# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html
import time

from scrapy import signals
from scrapy.http import HtmlResponse

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter


class WangyiproDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.
        # print('request middleware')

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    #  拦截板块详情页响应对象，修改为符合需求的对象
    def process_response(self, request, response, spider):
        #  获取在爬虫中定义的浏览器对象
        # print('开始拦截...')
        bro = spider.bro
        urls = []
        for url in spider.section_urls:
            urls.append(url['url'])
        # Called with the response returned from the downloader.
        #  筛选对应的响应对象
        if request.url in urls:
            # response 板块详情页响应对象
            # 实例化新的响应对象，包含动态加载的数据
            '''
                如何获取动态加载的响应数据？
                selenium
            '''
            bro.get(url=request.url)
            bro.execute_script("window.scrollBy(0,6000)")
            time.sleep(1)
            bro.execute_script("window.scrollBy(0,13000)")
            bro.implicitly_wait(30)  # 隐形等待最长30s
            page_text = bro.page_source # 获取动态加载的新闻数据
            new_res = HtmlResponse(url=request.url, body=page_text, encoding='utf-8', request=request)
            return new_res
        else:
            # print('Middleware no filter:', request.url)
            return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        return None
