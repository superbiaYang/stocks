import datetime
import logging
import math

import mysql.connector
import tushare as ts

logging.basicConfig(filename="stocks.log", level=logging.DEBUG, filemode="w")
logger = logging.getLogger()


def create_cnx():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="",
        database="stocks"
    )


def update_stocks():
    logger.info("开始更新股票列表")
    data = ts.get_stock_basics()
    cnx = create_cnx()
    cursor = cnx.cursor(prepared=True)
    stmt = "insert into stocks values (%s,%s) on duplicate key update name=%s;"

    for key, row in data.iterrows():
        stock_code = key
        stock_name = row['name']
        logger.debug("%s:%s" % (stock_code, stock_name))
        cursor.execute(stmt, (stock_code, stock_name, stock_name))

    cnx.commit()
    cursor.close()
    cnx.close()
    logger.info("获取股票列表完成")


def get_stocks():
    cnx = create_cnx()
    cursor = cnx.cursor()
    sql = "SELECT code FROM stocks;"
    cursor.execute(sql)
    data = cursor.fetchall()
    stocks = [row[0] for row in data]
    cursor.close()
    cnx.close()
    return stocks


def update_daily_hist():
    logger.info("开始更新每日数据历史")
    cnx = create_cnx()

    def update_stock(stock_code):
        logger.info("开始获取%s..." % (stock_code))
        date_cursor = cnx.cursor()
        date_sql = "SELECT MAX(date) FROM daily_hist WHERE code=%s;" % (
            stock_code)
        date_cursor.execute(date_sql)
        result = date_cursor.fetchone()[0]

        def calc_next_date(date):
            return (datetime.timedelta(days=1) + date).strftime("%Y-%m-%d")
        start_date = calc_next_date(result) if result is not None else None
        logger.info("从%s开始获取%s每日交易信息" % (start_date, stock_code))
        date_cursor.close()
        data = ts.get_hist_data(stock_code, start=start_date)
        if data is None:
            logger.info("%s没有数据" % (stock_code))
            return
        if len(data) == 0:
            logger.info("%s没有新数据" % (stock_code))
            return
        logger.info("%s共获取到%d条数据，开始写入..." % (stock_code, len(data)))
        cursor = cnx.cursor(prepared=True)
        stmt = "insert ignore into daily_hist values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
        for key, row in data.iterrows():
            date = key
            params = (
                date,
                stock_code,
                row['open'],
                row['high'],
                row['close'],
                row['low'],
                row['volume'],
                row['p_change'],
                row['price_change'],
                row['ma5'],
                row['ma10'],
                row['ma20'],
                row['v_ma5'],
                row['v_ma10'],
                row['v_ma20'],
            )
            cursor.execute(stmt, params)
        cnx.commit()
        cursor.close()
        logger.info("完成获取%s" % (stock_code))

    stocks = get_stocks()
    for stock_code in stocks:
        update_stock(stock_code)

    cnx.close()
    logger.info("更新每日数据历史完成")


def update_fundamental_info(year, season):
    logger.info("开始更新基本面信息%d-%d" % (year, season))
    cnx = create_cnx()

    def update_table(table):
        logger.info("清理%s历史信息%d-%d" % (table, year, season))
        sql = "DELETE FROM %s WHERE year=%d and season=%d" % (
            table, year, season)
        cursor = cnx.cursor()
        cursor.execute(sql)
        cnx.commit()
        cursor.close()
        func_name = "get_%s_data" % (table)
        func = getattr(ts, func_name)
        data = func(year, season)
        cols = list(filter(lambda x: x != "name", data.columns))
        cols_str = ",".join(cols)
        col_num = len(cols)
        col_placeholders = []
        for _ in range(col_num):
            col_placeholders.append("%s")
        col_placeholders_str = ",".join(col_placeholders)
        sql = "INSERT IGNORE INTO {table}(year,season,{cols_str}) values ({year},{season},{col_placeholders_str})"
        sql = sql.format(table=table, cols_str=cols_str, year=year,
                         season=season, col_placeholders_str=col_placeholders_str)
        cursor = cnx.cursor(prepared=True)
        for _, row in data.iterrows():
            params = tuple([None if isinstance(row[col], float) and math.isnan(
                row[col]) else row[col] for col in cols])
            cursor.execute(sql, params)
        cnx.commit()
        cursor.close()
        logger.info("更新%s-%d-%d完成" % (table, year, season))
    tables = ['report', 'profit', 'operation',
              'growth', 'debtpaying',  'cashflow']
    for table in tables:
        update_table(table)
    logger.info("更新基本面信息完成%d-%d" % (year, season))
    cnx.close()


def daily_job():
    update_stocks()
    update_daily_hist()
    now = datetime.datetime.now()
    year = now.year
    month = now.month
    season = math.ceil(month / 3)
    last_year = year - 1 if season == 1 else year
    last_season = 4 if season == 1 else season - 1
    update_fundamental_info(year, season)
    update_fundamental_info(last_year, last_season)


def init_database():
    update_stocks()
    update_daily_hist()
    start_year = 1992
    start_season = 2
    now = datetime.datetime.now()
    end_year = now.year
    month = now.month
    end_season = math.ceil(month / 3)
    year = start_year
    season = start_season
    while year*10 + season <= end_year*10+end_season:
        update_fundamental_info(year, season)


if __name__ == "__main__":
    import sys
    if len(sys.argv) == 0:
        daily_job()
    elif len(sys.argv) == 1 and sys.argv[1] == "init":
        init_database()
    else:
        print("USAGE: python stocks.py [init]")
