import argparse
import logging

from apscheduler.schedulers.twisted import TwistedScheduler
from scrapy.crawler import CrawlerProcess
from scrapy.utils.log import configure_logging
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


if __name__ == '__main__':
    configure_logging({'LOG_FORMAT': '%(levelname)s: %(message)s'})
    LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
    logging.basicConfig(
        level=logging.INFO,
        format=LOG_FORMAT
    )

    parser = argparse.ArgumentParser(description="股票行情爬虫")
    parser.add_argument("--cron", type=str, const=False, nargs='?', help="是否依照指定的时间执行，默认为False")
    parser.add_argument("--spider", type=str, default=None, help="选择调用的爬虫，不指定则公司信息爬虫和行情爬虫都调用，e.g. company")

    args = parser.parse_args()

    cron = str2bool(args.cron, False)
    spider = args.spider

    process = CrawlerProcess(get_project_settings())

    if not cron:
        if spider is None:
            spiders = [QuotesSpider, CompanyInfoSpider]
        elif spider == 'company':
            spiders = CompanyInfoSpider
        else:
            spiders = QuotesSpider
        process.crawl(spiders)
        process.start()
    else:
        scheduler = TwistedScheduler()

        if spider is None:
            spiders = [QuotesSpider, CompanyInfoSpider]
        elif spider == 'company':
            spiders = CompanyInfoSpider
        else:
            spiders = QuotesSpider

        scheduler.add_job(process.crawl,
                          'cron',
                          args=[spiders],
                          day_of_week='mon-fri',
                          hour='9-15',
                          minute='0/30')
        scheduler.start()
        process.start(False)
