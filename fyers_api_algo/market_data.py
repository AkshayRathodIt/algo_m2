from fyers_apiv3 import fyersModel
import os


def get_market_history_data(client_id, access_token):
    #   Initialize the FyersModel instance with your client_id, access_token, and enable async mode
    fyers = fyersModel.FyersModel(client_id=client_id, is_async=False, token=access_token, log_path="")

    # Make a request to get the user profile information
    try:
        data = {
            "symbol": "NSE:SBIN-EQ",
            "resolution": "15",
            "date_format": "1",
            "range_from": "2024-01-23",
            "range_to": "2024-01-23",
            "cont_flag": "1"
        }
        response = fyers.history(data)
        if response["code"] == 200:
            # print(response["data"])
            return response["candles"]
        else:
            return response["message"]+" something wrong happened"
    except Exception as e:
        return str(e)


# get historical data as json or list from fyers
def get_historical_data_json(access_tokan, client_id, symbol="NSE:TCS-EQ", resolution="5", start_date="2023-04-01",
                             end_date="2023-05-04"):
    fyers = fyersModel.FyersModel(client_id=client_id, is_async=False, token=access_tokan, log_path="")

    data = {
        "symbol": symbol,
        "resolution": resolution,
        "date_format": "1",
        "range_from": start_date,
        "range_to": end_date,
        "cont_flag": "1"
    }
    try:
        response = fyers.history(data=data)
        return [1, response]
    except Exception as e:
        return [-1, e]



