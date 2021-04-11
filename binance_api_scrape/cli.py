import click

from sqlalchemy import create_engine
from inireader import reader

from binance_api_scrape.schema import init_db, insert_db
from binance_api_scrape.scraper import Scraper

cfg = reader('binance.cfg')
DBURI = cfg['postgresql']['dburi']

@click.group()
def binance():
    pass

@binance.command('ping')
def ping():
    # register all component schemas
    scraper = Scraper()
    print(scraper.ping())

@binance.command('init-db')
def initdb():
    # register all component schemas
    engine = create_engine(DBURI)
    init_db(engine)


def _scrape():
    scraper = Scraper()
    engine = create_engine(DBURI)
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
def scrape():
    return _scrape()

