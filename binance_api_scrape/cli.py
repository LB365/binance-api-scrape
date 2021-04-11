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
        return os.environ.get('DATABASE_URL')
    

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


def _scrape(heroku):
    scraper = Scraper()
    mydburi = dburi(heroku)
    engine = create_engine(mydburi)
    mark = scraper.mark('BTC-210430-68000-C')
    print(mark)
    with engine.begin() as cn:
        for m in mark['data']:
            m['ts'] = mark['ts']
            insert_db(
                cn,
                'market.mark',
                m
            )
        


@binance.command('scrape')
@click.option('-heroku', is_flag=True)
def scrape(heroku):
    return _scrape(heroku)

