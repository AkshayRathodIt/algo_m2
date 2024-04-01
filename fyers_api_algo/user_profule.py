from fyers_apiv3 import fyersModel


def get_profile(client_id, access_token):
    #   Initialize the FyersModel instance with your client_id, access_token, and enable async mode
    fyers = fyersModel.FyersModel(client_id=client_id, is_async=False, token=access_token, log_path="")

    # Make a request to get the user profile information
    try:
        response = fyers.get_profile()
        if response["code"] == 200:
            # print(response["data"])
            return response["data"]
        else:
            return response["message"]+" something wrong happened"
    except Exception as e:
        return str(e)



