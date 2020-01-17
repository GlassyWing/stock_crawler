import argparse
import logging

from apscheduler.schedulers.twisted import TwistedScheduler
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from stock_crawler.spiders.company_info import CompanyInfoSpider
from stock_crawler.spiders.quotes import QuotesSpider


def str2bool(v, default=False):
    if v is None or len(v) == 0:
        return default
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Unsupported value encountered.')


def sequence_run():
    dfd = process.crawl(QuotesSpider)
    dfd.addCallback(lambda _: process.crawl(CompanyInfoSpider))


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="股票行情爬虫")
    parser.add_argument("--cron", type=str, const=False, nargs='?', help="是否依照指定的时间执行，默认为False")

    args = parser.parse_args()

    cron = str2bool(args.cron, False)

    process = CrawlerProcess(get_project_settings())

    # 设置日志级别
    logging.getLogger('scrapy.core.scraper').setLevel(logging.WARNING)

    if not cron:
        sequence_run()
        process.start()
    else:
        scheduler = TwistedScheduler()

        scheduler.add_job(sequence_run,
                          'cron',
                          day_of_week='mon-fri',
                          hour='9-15',
                          minute='0/30')
        scheduler.start()
        process.start(False)
