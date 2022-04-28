## scrapy框架
- 什么是框架
    集成了很多功能，并且具有很强的通用性的项目模板
- 如何学习框架
- 什么是scrapy
    - 爬虫中封装好的“明星”框架，封装程度高，使用频率高
    - 功能：
        - 高性能持久化存储
        - 异步数据下载
        - 高性能数据解析
        - 分布式
    - 基本使用
        - 环境安装
            - mac、Linux: `pip install scrapy`
            - windows:
                - `pip install wheel`
                - 下载安装twisted
                - `pip install pywin32`
                - `pip install scrapy`
        - 创建工程：`scrapy startproject xxxPro`
        - 执行工程：`scrapy crawl sipderName`
- 数据解析
    - `response.xpath()`
    - `extract()`
    - `extract_first()`
- 持久化存储
    - 基于终端指令：
        - 要求：只可以将parse()方法的返回值存储到本地的文本文件中
        - 步骤：将parse中需要存储的数据包装起来并作为返回值进入return
        - 注意：持久化对应的文本文件类型只能是：json、csv、jl、jsonlines、marshal、pickle等
        - 好处：简洁、高效、便捷
        - 缺点：局限性强，数据只能存储为指定后缀的文本文件，且只能存储parse封装好的指定数据
    - 基于管道：
        - 编码流程：
            - 数据解析
            - 将解析的数据封装存储到item类型的对象
- 手动发送请求
    - `yield scrapy.Request(url, callback)`

- 五大核心组件
    - 引擎（接收数据流&触发事务）
        - 引擎将请求对象发送给调度器的过滤器
        - 从调度器的队列中获取请求对象并发送给下载器
        - 将Response发送给Spider的parse
        - 接受parse解析好的数据并发送给管道
    - 爬虫类（Spider）
        - 产生url，封装为请求对象发送给 引擎 ，并进行请求发送
        - 调用parse进行数据解析并发送给引擎
    - 管道
        - 接收引擎发送的解析好的数据进行持久化存储
    - 下载器
        - 进行数据下载获取Response
        - 提交Response至引擎
    - 调度器
        - 过滤器
            对重复的请求对象进行去重，将去重后的请求对象发送到队列
        - 队列
    问题：引擎是如何触发事务的？
        - 引擎通过接收到的不同数据流类型判断事务类型
- 请求传参
    - 使用场景：爬取解析的数据不在同一张页面中。（深度爬取）
    - 需求：爬取Boss直聘岗位名称与岗位描述
    
- 图片数据爬取之ImagesPipeline
    - 基于字符串和基于图片的区别
        - 字符串： 只需要基于xpath进行解析且提交管道并进行持久化
        - 图片： xpath解析出图片src的属性值，单独对图片地址发起请求获取图片二进制类型的数据
    - ImagesPipeline:
        - 只需要将img的src的属性值进行解析，提交到管道，管道就会对图片的src进行请求发送获取图片的二进制数据，且还会帮我们进行持久化存储
        - 需求：爬取站长素材的高清图片
        - 使用流程：
            - 解析图片地址（懒加载）
            - 将存储图片地址的item提交到指定的管道类
            - 在管道文件中定制一个基于ImagesPipeline的管道类
                - `get_media_request()`
                - `file_path()`
                - `item_completed()`
            - 在配置文件中：
                - 指定文件存储目录: `IMAGES_STORE = '[path]'`
                - 指定开启的管道： 自定制的管道类
        - 遇到的问题：
            - item提交给管道后，管道不接收图片，死活没有反应: `INFO: Crawled 0 pages (at 0 pages/min), scraped 0 items (at 0 items/min)`
            - LOG_LEVEL = 'DEBUG'后看到一条警告: 
    `WARNING: Disabled ImgsPipeline: ImagesPipeline requires installing Pillow 4.0.0 or later`于是就赶紧安装了Pillow, 问题得以解决
              
- 中间件
    - 爬虫中间件
    - 下载中间件
        - 位置：引擎和下载器之间
        - 功能：批量拦截整个工程中所有的请求和响应
        - 拦截请求：
            - 进行UA伪装（可以对指定的请求进行专门的UA伪装）
            - 代理IP的设定
        - 拦截响应：
            - 篡改响应数据、对象
            - 需求：爬取网易新闻数据（标题+内容）
                1. 通过首页解析出五大板块对应详情页的URL（直接爬取）
                2. 板块对应的新闻标题列表（动态加载）
                3. 通过解析每一条新闻详情页URL，获取详情页源码解析出新闻内容（直接爬取）