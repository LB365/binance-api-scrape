from pathlib import Path
from typing import Dict, Optional

import pandas as pd

from sqlhelp import sqlfile, insert, update, select

SQLFILE = Path(__file__).parent / 'schema.sql'


def init_db(engine, drop=False):
    """
    Initialise the posgres database by creating the schemas for the ticker
    database.
    Args:
        engine: a sql engine
        drop: boolean to drop all prices schema from the database
    """
    if drop:
        with engine.begin() as cn:
            cn.execute('drop schema if exists prices cascade;')
    with engine.begin() as cn:
        cn.execute('create schema if not exists market;')
        cn.execute(sqlfile(SQLFILE))


def insert_db(cn, tab, dictionary: Dict):
    """
    Insert a ticker in the database
    Args:
        cn: a sql engine connection
        tab: the table of interest
        dictionary: key values to insert
    """
    q = select('1').table(
        tab
    ).where(
        **dictionary
    ).limit(1)

    if q.do(cn).scalar():
        return

    q = insert(tab).values(
        **dictionary
    )
    q.do(cn)
