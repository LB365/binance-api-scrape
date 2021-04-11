import click
import os
from itertools import repeat

from sqlalchemy import create_engine
from inireader import reader
import pandas as pd
from tqdm.contrib.concurrent import thread_map

from binance_api_scrape.schema import init_db, insert_db
from binance_api_scrape.scraper import Scraper
from binance_api_scrape import OPTION_INFO_FIELDS, MARK_FIELDS, TICKER_FIELDS

def filter_dict(d, keys):
    return dict(filter(lambda x: x[0] in keys, d.items()))

@click.group()
def binance():
    pass


def dburi(heroku):
    if not heroku:
        cfg = reader('binance.cfg')
        return cfg['postgresql']['dburi']
    else:
        url = os.environ.get('DATABASE_URL').replace('postgres', 'postgresql')
        return url


@binance.command('ping')
def ping():
    # register all component schemas
    scraper = Scraper()
    print(scraper.ping())


@binance.command('init-db')
@click.option('-heroku', is_flag=True)
def initdb(heroku):
    # register all component schemas
    mydburi = dburi(heroku)
    engine = create_engine(mydburi)
    init_db(engine)


def mark(heroku, ts=None, *args, **kwargs):
    scraper = Scraper()
    mydburi = dburi(heroku)
    engine = create_engine(mydburi)
    datas = scraper.mark()
    print(pd.DataFrame.from_records(datas['data']).head(3))
    with engine.begin() as cn:
        for data in datas['data']:
            data['ts'] = datas['ts'] if ts is None else ts
            insert_db(
                cn,
                'market.mark',
                filter_dict(data, MARK_FIELDS)
            )


def ticker(heroku, ts=None, *args, **kwargs):
    scraper = Scraper()
    mydburi = dburi(heroku)
    engine = create_engine(mydburi)
    datas = scraper.ticker()
    print(pd.DataFrame.from_records(datas['data']).head(3))
    fields = ['open', 'high', 'low']
    with engine.begin() as cn:
        for data in datas['data']:
            data['ts'] = datas['ts'] if ts is None else ts
            for field in fields:
                data[field + 'Price'] = data[field]
                del data[field]
            insert_db(
                cn,
                'market.ticker',
                filter_dict(data, TICKER_FIELDS)
            )


def optioninfo(heroku, *args, **kwargs):
    scraper = Scraper()
    mydburi = dburi(heroku)
    engine = create_engine(mydburi)
    datas = scraper.option_info()
    print(pd.DataFrame.from_records(datas['data']).head(3))
    with engine.begin() as cn:
        for data in datas['data']:
            insert_db(
                cn,
                'market.optioninfo',
                filter_dict(data, OPTION_INFO_FIELDS)
            )


@binance.command('scrape')
@click.option('-scraper',
              type=click.Choice(['mark', 'ticker', 'optioninfo']))
@click.option('-heroku', is_flag=True)
def scrape(scraper, heroku):
    return eval(scraper)(heroku)


@binance.command('scrape_all')
@click.option('-heroku', is_flag=True)
def scrape(heroku):
    scraper = Scraper()
    ts = scraper.ts()
    return thread_map(
        lambda func, h, ts: func(h, ts),
        (mark, ticker, optioninfo),
        repeat(heroku),
        (ts, ts, None)
    )
