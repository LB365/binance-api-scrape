import click
import os

from sqlalchemy import create_engine
from inireader import reader

from binance_api_scrape.schema import init_db, insert_db
from binance_api_scrape.scraper import Scraper

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


def mark(heroku, ts=None):
    scraper = Scraper()
    mydburi = dburi(heroku)
    engine = create_engine(mydburi)
    mark = scraper.mark()
    with engine.begin() as cn:
        for data in mark['data']:
            data['ts'] = ticker['ts'] if ts is None else ts
            insert_db(
                cn,
                'market.mark',
                data
            )
        

def ticker(heroku, ts=None):
    scraper = Scraper()
    mydburi = dburi(heroku)
    engine = create_engine(mydburi)
    ticker = scraper.ticker()
    with engine.begin() as cn:
        for data in ticker['data']:
            data['ts'] = ticker['ts'] if ts is None else ts
            insert_db(
                cn,
                'market.ticker',
                data
            )

def optioninfo(heroku):
    scraper = Scraper()
    mydburi = dburi(heroku)
    engine = create_engine(mydburi)
    ticker = scraper.option_info()
    with engine.begin() as cn:
        for data in ticker['data']:
            insert_db(
                cn,
                'market.optioninfo',
                data
            )

@binance.command('scrape')
@click.option('-scraper',
              type=click.Choice(['mark', 'ticker', 'optioninfo']))
@click.option('-heroku', is_flag=True)
def scrape(scraper, heroku):
    return eval(scraper)(heroku)