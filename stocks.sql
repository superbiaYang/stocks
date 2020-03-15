create database stocks;

create table stocks(
    `code` char(6),
    `name` char(8),
    primary key (`code`)
);

create table daily_hist(
    `date` date,
    `code` char(6),
    `open` float,
    `high` float,
    `close` float,
    `low` float,
    `volume` float,
    `p_change` float,
    `price_change` float,
    `ma5` float,
    `ma10` float,
    `ma20` float,
    `v_ma5` float,
    `v_ma10` float,
    `v_ma20` float,
    primary key (`date`, `code`)
);

create table daily_hist(
    `date` date,
    `code` char(6),
    `open` float,
    `high` float,
    `close` float,
    `low` float,
    `volume` float,
    `p_change` float,
    `price_change` float,
    `ma5` float,
    `ma10` float,
    `ma20` float,
    `v_ma5` float,
    `v_ma10` float,
    `v_ma20` float,
    primary key (`date`, `code`)
);

create table report(
    `year` int,
    `season` int,
    `code` char(6),
    `eps` float,
    `eps_yoy` float,
    `bvps` float,
    `roe` float,
    `epcf` float,
    `net_profits` float,
    `profits_yoy` float,
    `distrib` varchar(16),
    `report_date` varchar(10),
    primary key (`year`, `season`, `code`)
);

create table profit(
    `year` int,
    `season` int,
    `code` float,
    `roe` float,
    `net_profit_ratio` float,
    `gross_profit_rate` float,
    `net_profits` float,
    `eps` float,
    `business_income` float,
    `bips` float,
    primary key (`year`, `season`, `code`)
);

create table operation(
    `year` int,
    `season` int,
    `code` char(6),
    `arturnover` float,
    `arturndays` float,
    `inventory_turnover` float,
    `inventory_days` float,
    `currentasset_turnover` float,
    `currentasset_days` float,
    primary key (`year`, `season`, `code`)
);

create table growth(
    `year` int,
    `season` int,
    `code` char(6),
    `mbrg` float,
    `nprg` float,
    `nav` float,
    `targ` float,
    `epsg` float,
    `seg` float,
    primary key (`year`, `season`, `code`)
);

create table debtpaying(
    `year` int,
    `season` int,
    `code` char(6),
    `currentratio` float,
    `quickratio` float,
    `cashratio` float,
    `icratio` float,
    `sheqratio` float,
    `adratio` float,
    primary key (`year`, `season`, `code`)
);

create table cashflow(
    `year` int,
    `season` int,
    `code` char(6),
    `cf_sales` float,
    `rateofreturn` float,
    `cf_nm` float,
    `cf_liabilities` float,
    `cashflowratio` float,
    primary key (`year`, `season`, `code`)
);