from fyers_apiv3 import fyersModel


def get_market_status(client_id, access_token):
    #   Initialize the FyersModel instance with your client_id, access_token, and enable async mode
    fyers = fyersModel.FyersModel(client_id=client_id, is_async=False, token=access_token, log_path="")

    # Make a request to get the user profile information
    try:
        response = fyers.market_status()
        if response["code"] == 200:
            # print(response["data"])
            return response["marketStatus"]
        else:
            return response["message"]+" something wrong happened"
    except Exception as e:
        return str(e)



