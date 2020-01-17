from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from stock_crawler.spiders.main_target import MainTargetSpider

if __name__ == '__main__':
    process = CrawlerProcess(get_project_settings())
    process.crawl(MainTargetSpider, companies=['688278'])
    process.start()