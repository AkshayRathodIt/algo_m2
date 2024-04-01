from fyers_api_algo.market_data import get_market_history_data, get_historical_data_json
from utils.read_json import read_json_file
from fyers_api_algo.fyers_app_login import get_access_tokan_final
import pandas as pd
import datetime as dt
from datetime import datetime, timedelta
import os
import time

json_file_path = 'config.json'  # Path to the JSON file in the project directory

path = os.path.dirname(os.path.abspath(__file__))
# print(os.getcwd())
config = read_json_file(json_file_path)

# login api
access_token = get_access_tokan_final(config, path)

# profile api
client_id = f"{config['APP_ID']}-{config['APP_TYPE']}"



# gate monthely date range for historical data
def get_monthly_date_ranges(start_date, end_date):
    """
    Return a list of tuples representing the first and last date of each month between the start_date
    and end_date, inclusive.

    Args:
        start_date (str): A string representing the start date in the format 'YYYY-MM-DD'
        end_date (str): A string representing the end date in the format 'YYYY-MM-DD'

    Returns:
        A list of tuples in the format ('YYYY-MM-DD', 'YYYY-MM-DD')
    """
    # Convert start and end dates to datetime objects
    start_date_obj = datetime.strptime(start_date, '%Y-%m-%d')
    end_date_obj = datetime.strptime(end_date, '%Y-%m-%d')

    # Initialize a list to hold the date ranges
    date_ranges = []

    # Loop through each month between start_date and end_date
    current_month = start_date_obj.replace(day=1)
    while current_month <= end_date_obj:
        # Get the last day of the current month
        next_month = current_month.replace(day=28) + timedelta(days=4)  # Add 4 days to handle edge cases
        last_day_of_month = next_month - timedelta(days=next_month.day)

        # Add the current month's date range to the list
        date_ranges.append([current_month.strftime('%Y-%m-%d'), last_day_of_month.strftime('%Y-%m-%d')])

        # Move to the next month
        current_month = next_month.replace(day=1)

    return date_ranges


# get full historical data from fyers
def get_full_historical_data(start_date, end_date, symbol, resolution="15"):
    date_list = get_monthly_date_ranges(start_date, end_date)
    # print(date_list)
    # print(end_date)
    json_list = []
    for item in date_list:
        json = get_historical_data_json(access_token, client_id, symbol, resolution=resolution, start_date=item[0],
                                        end_date=item[1])
        if json[0]:
            json_list += json[1]["candles"]
        time.sleep(0.2)

    ohlc_df = pd.DataFrame(json_list)
    column_names = ["time_stamp", "open", "high", "low", "close", "volume"]
    ohlc_df.columns = column_names

    # Converting epoch time to timestamp
    ohlc_df["time_stamp"] = pd.to_datetime(ohlc_df["time_stamp"], unit="s")

    # converting non standerd time to UTC time
    ohlc_df["time_stamp"] = ohlc_df["time_stamp"].dt.tz_localize("UTC")
    ohlc_df["time_stamp"] = ohlc_df["time_stamp"].dt.tz_convert("Asia/Kolkata").dt.strftime("%Y-%m-%d %H:%M:%S")

    updated_start_date = dt.datetime.strftime(pd.to_datetime(ohlc_df["time_stamp"].iloc[0]).date(), "%Y-%m-%d")
    end_date = end_date
    new_date_list = get_monthly_date_ranges(updated_start_date, end_date)
    new_date_list[-1][1] = end_date

    day_data = []
    for item in new_date_list:
        print(item)
        json = get_historical_data_json(access_token, client_id, symbol, "D", item[0], item[1])
        if json[0]:
            day_data += json[1]["candles"]
        time.sleep(1)

    ohlc_day_df = pd.DataFrame(day_data)
    column_names = ["time_stamp", "open", "high", "low", "close", "volume"]
    ohlc_day_df.columns = column_names
    ohlc_day_df["time_stamp"] = pd.to_datetime(ohlc_day_df["time_stamp"], unit="s")
    ohlc_day_df["time_stamp"] = ohlc_day_df["time_stamp"].dt.tz_localize("UTC")
    ohlc_day_df["time_stamp"] = ohlc_day_df["time_stamp"].dt.tz_convert("Asia/Kolkata").dt.strftime("%Y-%m-%d %H:%M:%S")

    df = ohlc_df.set_index(pd.to_datetime(ohlc_df.time_stamp))
    df["date"] = df.index.date

    df1 = ohlc_day_df.set_index(pd.to_datetime(ohlc_day_df.time_stamp))
    df1["date"] = df1.index.date

    final_df = df.merge(df1, how="inner", on="date", )
    final_df.drop(columns=["time_stamp_y", "open_y", "high_y", "low_y", "volume_y", "date"], inplace=True)
    final_df.rename(columns={"time_stamp_x": "time_stamp",
                             "open_x": "open",
                             "high_x": "high",
                             "low_x": "low",
                             "close_x": "close",
                             "volume_x": "volume",
                             "close_y": "adj_close",
                             }, inplace=True)

    # final_df.set_index(pd.to_datetime(df.time_stamp)).drop(columns="time_stamp", axis=1, inplace=True)

    return final_df



if __name__ == '__main__':
    df = get_full_historical_data("2018-06-01","2023-12-30","NSE:TCS-EQ", "10")
    print(df.count())
    print(df)