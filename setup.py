from setuptools import find_packages, setup
from pathlib import Path
HERE = Path(__file__).parent

REQUIREMENTS = [
    "pandas",
    "sqlalchemy",
    "sqlhelp",
    "click",
    "requests",
    "psycopg2",
    "inireader",
]

setup(
    name='binance-api-scrape',
    author='Loïc Balland',
    version='0.1.0',
    description='scrape binance option market data',
    packages=find_packages(include=['binance_api_scrape']),
    entry_points={
        'console_scripts': [
            'binance=binance_api_scrape.cli:binance',
        ]
    },
    install_requires=REQUIREMENTS,
)
