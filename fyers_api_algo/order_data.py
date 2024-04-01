from fyers_apiv3 import fyersModel


def get_order_data(client_id, access_token):
    #   Initialize the FyersModel instance with your client_id, access_token, and enable async mode
    fyers = fyersModel.FyersModel(client_id=client_id, is_async=False, token=access_token, log_path="")

    # Make a request to get the user profile information
    try:
        response = fyers.orderbook()
        if response["code"] == 200:
            # print(response["data"])
            return response["orderBook"]
        else:
            return response["message"]+" something wrong happened"
    except Exception as e:
        return str(e)


def get_order_data_by_tag(client_id, access_token, orderId):
    #   Initialize the FyersModel instance with your client_id, access_token, and enable async mode
    fyers = fyersModel.FyersModel(client_id=client_id, is_async=False, token=access_token, log_path="")

    # Make a request to get the user profile information
    try:
        data = {"id": orderId}
        response = fyers.orderbook(data=data)
        if response["code"] == 200:
            # print(response["data"])
            return response["orderBook"]
        else:
            return response["message"]+" something wrong happened"
    except Exception as e:
        return str(e)


