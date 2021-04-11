create table if not exists market.optioninfo (
  id serial primary key,
  ts timestamptz not null,
  underlying text not null,
  quoteAsset text not null,
  symbol text not null,
  unit int not null,
  minQty int not null,
  side text not null,
  leverage real not null,
  strikePrice real not null,
  expiryDate int not null
);

create table if not exists market.mark (
  id serial primary key,
  ts timestamptz not null,
  symbol text not null,
  markPrice real not null,
  bidIV real not null,
  askIV real not null,
  delta real not null,
  theta real not null,
  gamma real not null,
  vega real not null,
  volatility real not null,
  highPriceLimit real not null,
  lowPriceLimit real not null
);

create table if not exists market.ticker (
  id serial primary key,
  ts timestamptz not null,
  symbol text not null,
  priceChange real not null,
  priceChangePercent real not null,
  lastPrice real not null,
  lastQty real not null,
  openPrice real not null,
  highPrice real not null,
  lowPrice real not null,
  volume real not null,
  amount real not null,
  openTime real not null,
  closeTime real not null
);

