


import os
from utils.read_json import read_json_file
from fyers_api_algo.fyers_app_login import get_access_tokan_final
from fyers_api_algo.user_profule import get_profile
from fyers_api_algo.funds_data import funds_info
from fyers_api_algo.holding_data import get_holdings, get_overall
from fyers_api_algo.order_data import get_order_data
from fyers_api_algo.position_data import get_poditiond, get_overall_positions
from fyers_api_algo.tread_data import get_treade_data
from fyers_api_algo.market_status_data import get_market_status
from market_data_db.connect import connect_to_mysql
from market_data_db.watchlist_table import create_watchlist_table, insert_into_watchlist, delete_from_watchlist_by_fyers_symbol, get_fyers_symbols_by_strategy
from fyers_api_algo.market_data import get_market_history_data
from market_data_db.ticker_tables import create_tables_for_tickres

if __name__ == "__main__":
    json_file_path = 'config.json'  # Path to the JSON file in the project directory

    path = os.path.dirname(os.path.abspath(__file__))
    # print(os.getcwd())
    config = read_json_file(json_file_path)

    # login api
    access_token = get_access_tokan_final(config, path)

    # profile api
    client_id = f"{config['APP_ID']}-{config['APP_TYPE']}"

    print("profile")
    profile = get_profile(client_id, access_token)
    print(profile)

    # funds api
    print("funds")
    funds = funds_info(client_id, access_token)
    print(funds)

    # holdings api
    print("holdings")
    holdings = get_holdings(client_id, access_token)
    print(holdings)

    print("overall")
    overall = get_overall(client_id, access_token)
    print(overall)



    print("position")
    position = get_poditiond(client_id, access_token)
    print(orders)

    print("overall position")
    overall_position = get_overall_positions(client_id, access_token)
    print(orders)

    print("treade data")
    treads = get_treade_data(client_id, access_token)
    print(orders)

    print("Market status")
    markrt_status = get_market_status(client_id, access_token)
    print(markrt_status)

    print("connect to mysql")
    conn = connect_to_mysql("localhost","root", "Harshada07@1999","algo_m2")

    print("watchlist")
    create_watchlist_table(conn)

    print("insert stoke in watchlist")
    data_to_insert = {
        'fyers_id': 101000000011536,
        'detail_symbol': 'TATA CONSULTANCY SERV LT',
        'minimum_lot_size': 1,
        'minimum_tick_size': 0.05,
        'ISIN': 'INE467B01029',
        'Fyers_symbol': 'NSE:TCS-EQ',
        'exchange': 10,
        'strategy': 'str1'
    }
    insert_into_watchlist(conn, data_to_insert)

    print("delete from row")
    # delete_from_watchlist_by_fyers_symbol(conn, "NSE:MARUTI-EQ")

    print("all list of fyers")
    tickers_list =get_fyers_symbols_by_strategy(conn, "str1")
    print(tickers_list)

    print("get history market data")
    market_data = get_market_history_data(client_id, access_token)
    print(market_data)

    print("create tables for tickers")
    create_tables_for_tickres(conn, tickers_list)

    print("get historical data for tcs")
    from historical_data_adjested import get_full_historical_data
    df = get_full_historical_data("2018-06-01","2023-12-29","NSE:TCS-EQ","10")
    print(df)

    print("add data to tickers tables")
    from market_data_db.ticker_tables import insert_data_into_table, get_data_for_specific_day
    # insert_data_into_table(conn, df, "NSE:TCS-EQ")

    # get data for a specific date
    print("date wise data")
    result = get_data_for_specific_day(conn,"NSE:TCS-EQ","2023-12-29")
    print(result)




