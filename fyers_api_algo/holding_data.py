from fyers_apiv3 import fyersModel


def get_holdings(client_id, access_token):
    #   Initialize the FyersModel instance with your client_id, access_token, and enable async mode
    fyers = fyersModel.FyersModel(client_id=client_id, is_async=False, token=access_token, log_path="")

    # Make a request to get the user profile information
    try:
        response = fyers.holdings()
        # print(response)
        if response["code"] == 200:
            # print(response["data"])
            return response["holdings"]
        else:
            return response["message"]+" something wrong happened"
    except Exception as e:
        return str(e)

def get_overall(client_id, access_token):
    #   Initialize the FyersModel instance with your client_id, access_token, and enable async mode
    fyers = fyersModel.FyersModel(client_id=client_id, is_async=False, token=access_token, log_path="")

    # Make a request to get the user profile information
    try:
        response = fyers.holdings()
        if response["code"] == 200:
            # print(response["data"])
            return response["overall"]
        else:
            return response["message"]+" something wrong happened"
    except Exception as e:
        return str(e)

