from setuptools import find_packages, setup

setup(
    name='binance-api-scrape',
    author='Loïc Balland',
    version='0.1.0',
    description='scrape binance option market data',
    packages=find_packages(include=['binance_api_scrape']),
    python_requires='<=3.9',
     entry_points={
        'console_scripts': [
            'binance=binance_api_scrape.cli:binance',
        ]
    },
    install_requires=[
        'pytest',
        'pandas',
        'numpy',
        'sqlalchemy',
        'sqlhelp',
        'inireader',
    ],
)
