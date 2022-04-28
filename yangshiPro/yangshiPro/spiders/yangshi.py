import json
import re
from yangshiPro.items import YangshiproItem
import scrapy
import time


def get_current_time():
    return time.strftime('%Y-%m-%d')


def is_valid_url(item):
    # if 'ARTIxxLe2vhAhId7G3nphaBc220416' in url:
    #     return True
    # else:
    #     return False
    """
        过滤掉非法链接
    """
    is_valid = False
    # 筛选当天新闻
    if get_current_time() in item['focus_date']:
        is_valid = True
    # 过滤掉含有无法解析内容的链接
    valid_arr = ['photo']
    for i in valid_arr:
        if i in item['url']:
            is_valid = False
    return is_valid


def is_valid_body(response):
    body = response.xpath('//*[@id="page_body"]').extract_first()
    if body is None:
        return False
    return True


def get_origin_time(node):
    info_str = "".join(node.xpath('//*[@class="info"]//text()').extract())
    info_node = node.xpath('//*[@class="info"]/span//text()').extract_first()
    if "|" in info_str:
        # 字符串中存在 |， 先从其中计算出时间，然后从母串中替换掉时间部分，分割字符串
        timeline = re.findall(pattern=r'20?.* ?.*:[0-9]{2}', string=info_str)[0]
        origin = info_str.replace(timeline, "").split(" ")[0].split("：")[1]
    elif info_node == None:
        # 针对旧样式，从info 的 i 标签中读取信息
        # info_node = node.xpath('//*[@class="info"]/i//text()').extract()
        origin = node.xpath('//*[@class="info"]/i//text()').extract_first().split(" ")[0].split("：")[1]
    else:
        # 适配部分文娱新闻的样式
        info_node = node.xpath('//*[@class="info"]/span//text()').extract()
        origin = info_node[0]
    return origin


def get_content(response):
    body = is_valid_body(response)
    origin = get_origin_time(response)
    if not body:
        content = response.xpath('//*[@id="text_area"]').extract_first()
    else:
        content = response.xpath('//*[@id="content_area"]').extract_first()
    content = ''.join(content)
    content = re.sub('\n', '', content)
    content = re.sub('\s', '', content)
    # 取出传入的item，填充完整信息
    item = response.meta['item']
    item['content'] = content
    item['origin'] = origin
    item['timeline'] = item['focus_date']
    yield item


class YangshiSpider(scrapy.Spider):
    name = 'yangshi'
    # allowed_domains = ['www.yangshi.com']
    start_urls = ['https://news.cctv.com']
    base_urls = 'https://news.cctv.com/2019/07/gaiban/cmsdatainterface/page/'

    section_urls = [
        {"url": 'ent', "name": '文娱'},
        {"url": 'life', "name": '生活'},
        {"url": 'health', "name": '健康'},
        {"url": 'law', "name": '法律'},
        {"url": 'economy_zixun', "name": '财经'},
        {"url": 'society', "name": '社会'},
        # {"url": 'china', "name": '国内'},
        {"url": 'tech', "name": '科技'},
        {"url": 'world', "name": '世界'},
    ]

    def parse(self, response):
        for section in self.section_urls:
            category = section['name']
            for i in range(1, 7):
                url = self.get_full_url(section['url'], i)
                yield scrapy.Request(url=url, callback=self.get_news_list, meta={"category": category})

    def get_news_list(self, response):
        if response.status == 200:
            text = re.search(pattern=r'[{^].*[}]', string=response.text).group(0)
            news_list = json.loads(text)
            news_list = news_list['data']['list']
            # 解析得到新闻列表
            for news in news_list:
                item = json.loads(json.dumps(news), object_hook=YangshiproItem)
                item['category'] = response.meta['category']
                if is_valid_url(item):
                    print('Request:', item['url'])
                    yield scrapy.Request(url=item['url'], callback=get_content, meta={"item": item})
                else:
                    continue
        else:
            raise ChildProcessError("请求超界！", response.url)

    # 获取完整url
    def get_full_url(self, section, index):
        url = f'{self.base_urls}{section}_{index}.jsonp?cb={section}'
        return url
