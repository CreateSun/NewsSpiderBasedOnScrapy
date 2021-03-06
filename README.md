# NewsSpiderBasedOnScrapy
## 通过Scrapy与Selenium结合，爬取网易新闻与央视新闻中的新闻数据（包含已经爬到的近4k条数据）

> 参考视频来自B站：https://www.bilibili.com/video/BV1ha4y1H7sx?share_source=copy_web

## 运行方式
导入到Pycharm中，打开__init__.py文件后直接运行即可
**Warning:** 可能会出现selenium找不到chorme.driver的错误，这是因为项目的运行依赖浏览器内核，这个需要自己配置浏览器内核一下路径，并且内额版本应该与自己电脑上的浏览器版本兼容。内核下载地址：http://chromedriver.storage.googleapis.com/index.html
## 主要功能
+ 获取特定分区内容
+ 获取特定时间段内的内容
+ 新闻数据模型保存在item.py文件中
## 实现逻辑
### 网易新闻
**主要思路是从主站获取各个分区的URL，过滤掉部分不合规的URL（图片新闻等）后，请求分区新闻列表。由于网易新闻的分区列表是动态加载，所以在处理分区的列表数据时，通过Scrapy的中间件模块调用Selenium启动浏览器内核，通过软加载、下拉页面的方式获取页面列表数据传回Spider模块，分析出新闻列表，最后一次请求没个详情页获取新闻数据保存至csv中**
### 央视新闻
**央视新闻的API比较简单，可以通过开发者工具直接抓取到每个分区的新闻列表请求地址，通过遍历地址就可以分方便地获取到新闻信息。**
