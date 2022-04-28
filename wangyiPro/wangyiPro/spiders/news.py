import time

import scrapy
from selenium.webdriver import Chrome, ChromeOptions
from wangyiPro.items import WangyiproItem
import re


def get_current_time():
    return time.strftime('%Y-%m-%d')


# todo 筛选出正确的新闻
def is_valid_item(item):
    timeline = item['timeline']
    is_valid = False
    # if get_current_time() in timeline:
    #     is_valid = True
    if "div" not in item['content']:
        return False
    return True


# 屏蔽无法解析的新闻详情链接
def is_true_news(url):
    error_params = ['nba.sports', 'video', 'photo', 'live']
    is_valid = True
    for i in error_params:
        if i in url:
            is_valid = False
            return is_valid
    return is_valid


# 屏蔽无法解析的板块
def is_true_section(section):
    error_name_list = ['图片', '严选', '公益', '政务', '山西', '网易号', '车', '公开课', '直播', '科学', '红彩', '经典', '二手房', '本地', '身体课']
    error_url_list = ['photo', 'gongyi', 'gov', 'sx', 'dy.163', 'product', 'open', 'v.163.com', 'hongcai', 'public.163']
    is_valid = True
    for i in error_name_list:
        if i in section['name']:
            is_valid = False
    for i in error_url_list:
        if i in section['url']:
            is_valid = False
    return is_valid


def parse_detail(response):
    item = response.meta['item']
    timeline = response.xpath('//div[@class="post_info"]/text()').extract_first()
    timeline = timeline.split('来源')[0]
    timeline = re.findall(pattern=r'20?.* ?.*:[0-9]{2}', string=timeline)[0]
    item['timeline'] = timeline
    content = response.xpath('//*[@id="content"]/div[2]').extract()
    content = ''.join(content)
    content = re.sub('\n', '', content)
    content = re.sub(',', '，', content)
    keywords = response.xpath('//head/meta[@name ="keywords"]/@content').extract_first().replace(",", "|").replace(
        "，", "|")
    if 'dy' in response.url or 'news' in response.url:
        origin = response.xpath('//*[@class="post_info"]/a[1]/text()').extract_first()
    else:
        origin = response.xpath('//*[@class="post_info"]/text()').extract_first()
        origin = origin.split("来源: ")[1].replace(" ", "").replace("\n", "")
    item['content'] = content
    item['keywords'] = keywords
    item['origin'] = origin
    if is_valid_item(item):
        print(item['timeline'], item['category'], item['title'])
        yield item


def parse_section(response):
    with open('./page.html', 'w', encoding='utf-8') as fp:
        fp.write(response.text)
    div_list = response.xpath('//div[@class="ndi_main"]/div')
    category = response.meta['category']
    # print(div_list[0])
    for div in div_list:
        title = div.xpath('./div//h3/a/text()').extract_first()
        detail_url = div.xpath('./div//h3/a//@href').extract_first()
        # print(title, detail_url)
        # 跳过非正常新闻页面
        if detail_url is None or not is_true_news(detail_url): continue
        item = WangyiproItem()
        item['title'] = title
        item['category'] = category
        yield scrapy.Request(url=detail_url, callback=parse_detail, meta={"item": item})


class NewsSpider(scrapy.Spider):
    name = 'news'
    # allowed_domains = ['www.xxx.com']
    # start_urls = ['https://news.163.com/']
    start_urls = ['https://www.163.com/']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        options = ChromeOptions()
        options.add_experimental_option("excludeSwitches", ['enable-automation'])
        options.add_argument("--ignore-certificate-error")
        options.add_argument("--ignore-ssl-errors")
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        self.bro = Chrome(executable_path='D:\\Project\\python\\scrapy-test\\5.动态加载数据处理\\chromedriver.exe',
                          chrome_options=options)

    # 解析五大板块对应详情页的url
    section_urls = []

    def parse(self, response):
        li_list = response.xpath('//*[@id="js_index2017_wrap"]/div[2]/div[1]/div[2]/ul/li')
        for new_list in li_list:
            for item in new_list.xpath('./a'):
                name = item.xpath('./text()').extract_first()
                url = item.xpath('./@href').extract_first()
                section = {
                    "name": name,
                    "url": url
                }
                if is_true_section(section):
                    self.section_urls.append(section)
        # 依次对每个板块对应的页面进行请求
        # todo 测试
        new_list = self.section_urls
        # new_list = [self.section_urls[7]]
        for item in new_list:
            yield scrapy.Request(url=item['url'], callback=parse_section,
                                 meta={"url": item['url'], "category": item['name']})

    # 解析新闻标题和详情页url

    def closed(spider, reason):
        spider.bro.quit()
        pass
