import json
import requests
import time
import pyotp
import os
from urllib.parse import parse_qs, urlparse
import sys
from fyers_apiv3 import fyersModel
from urllib import parse
import os
import  datetime


BASE_URL = "https://api-t2.fyers.in/vagator/v2"
BASE_URL_2 = "https://api.fyers.in/api/v2"
URL_SEND_LOGIN_OTP = BASE_URL + "/send_login_otp"
URL_VERIFY_TOTP = BASE_URL + "/verify_otp"
URL_VERIFY_PIN = BASE_URL + "/verify_pin"
URL_TOKEN = BASE_URL_2 + "/token"
SUCCESS = 1
ERROR = -1

def send_login_otp(fy_id, app_id):
    try:
        result_string = requests.post(url=URL_SEND_LOGIN_OTP, json= {"fy_id": fy_id, "app_id": app_id })
        if result_string.status_code != 200:
            return [ERROR, result_string.text]
        result = json.loads(result_string.text)
        request_key = result["request_key"]
        return [SUCCESS, request_key]
    except Exception as e:
        return [ERROR, e]

# generate totp
def generate_totp(secret):
    try:
        generated_totp = pyotp.TOTP(secret).now()
        return [SUCCESS, generated_totp]

    except Exception as e:
        return [ERROR, e]

# verify otp function
def verify_totp(request_key, totp):
    try:
        payload = {
            "request_key": request_key,
            "otp": totp
        }

        result_string = requests.post(url=URL_VERIFY_TOTP, json=payload)
        if result_string.status_code != 200:
            return [ERROR, result_string.text]

        result = json.loads(result_string.text)
        request_key = result["request_key"]

        return [SUCCESS, request_key]

    except Exception as e:
        return [ERROR, e]

# verify pin
def verify_PIN(request_key, pin):
    try:
        payload = {
            "request_key": request_key,
            "identity_type": "pin",
            "identifier": pin
        }

        result_string = requests.post(url=URL_VERIFY_PIN, json=payload)
        if result_string.status_code != 200:
            return [ERROR, result_string.text]

        result = json.loads(result_string.text)
        access_token = result["data"]["access_token"]

        return [SUCCESS, access_token]

    except Exception as e:
        return [ERROR, e]

# get auth code
def token(fy_id, app_id, redirect_uri, app_type, access_token):
    try:
        payload = {
            "fyers_id": fy_id,
            "app_id": app_id,
            "redirect_uri": redirect_uri,
            "appType": app_type,
            "code_challenge": "",
            "state": "sample_state",
            "scope": "",
            "nonce": "",
            "response_type": "code",
            "create_cookie": True
        }
        headers = {'Authorization': f'Bearer {access_token}'}

        result_string = requests.post(
            url=URL_TOKEN, json=payload, headers=headers
        )

        if result_string.status_code != 308:
            return [ERROR, result_string.text]

        result = json.loads(result_string.text)
        url = result["Url"]
        auth_code = parse.parse_qs(parse.urlparse(url).query)['auth_code'][0]
        print("auth")
        return [SUCCESS, auth_code]

    except Exception as e:
        print("not auth")
        return [ERROR, e]


def get_final_access_tokan(auth_code, config):

    session = fyersModel.SessionModel(
        client_id=f"{config['APP_ID']}-{config['APP_TYPE']}",
        secret_key=config["SECRET_KEY"],
        redirect_uri=config["REDIRECT_URI"],
        response_type="code",
        grant_type="authorization_code"
    )

    # Set the authorization code in the session object
    session.set_token(auth_code)

    # Generate the access token using the authorization code
    response = session.generate_token()

    if response["code"] ++ 200:
        return  [SUCCESS, response["access_token"]]
    else:
        return  [ERROR, "token not generated"]

def login_to_fyers(config):
    FY_ID = config["FY_ID"]
    APP_ID_TYPE =config["APP_ID_TYPE"]
    TOTP_KEY= config["TOTP_KEY"]
    PIN = config["PIN"]
    APP_ID = config["APP_ID"]
    REDIRECT_URI = config["REDIRECT_URI"]
    APP_TYPE = config["APP_TYPE"]

    # Step 1 to get to the login page
    request_key_1 =send_login_otp(FY_ID, APP_ID_TYPE)
    my_requestkey_1 = request_key_1[1]
    if request_key_1[0] != SUCCESS:
        print(f"send_login_otp failure - {my_requestkey_1}")
        sys.exit()
    else:
        print("send_login_otp success")

    # Step 2 - Generate totp
    totp = generate_totp(TOTP_KEY)
    my_totp =totp[1]
    if totp[0] != SUCCESS:
        print(f"generate_totp failure - {totp[1]}")
        sys.exit()
    else:
        print("generate_totp success")

    # Step 3 - Verify totp and get request key from verify_otp API
    for i in range(1,3):
        request_key = my_requestkey_1
        verify_totp_result = verify_totp(request_key=request_key, totp=my_totp)
        if verify_totp_result[0] != SUCCESS:
            print(f"verify_totp_result failure - {verify_totp_result[1]}")
            time.sleep(1)
        else:
            print(f"verify_totp_result success {verify_totp_result}")
            break

    request_key_2 = verify_totp_result[1]

    # Step 4 - Verify pin and send back access token
    access_tokan = verify_PIN(request_key_2,PIN)
    access_tokan_1 = access_tokan[1]
    if access_tokan[0] != SUCCESS:
        print(f"verify_pin_result failure - {access_tokan[1]}")
        sys.exit()
    else:
        print("verify_pin_result success")

    print(access_tokan_1)

    # # Step 5 - Get auth code for API V2 App from trade access token
    auth_code = token(FY_ID, APP_ID,REDIRECT_URI,APP_TYPE,access_tokan_1)
    auth_code_final = auth_code[1]
    if auth_code[0] != SUCCESS:
        print(f"token_result failure - {auth_code[1]}")
        sys.exit()
    else:
        print("token_result success")


    access_token_final = get_final_access_tokan(auth_code_final, config)
    return  access_token_final

def get_access_tokan_final(config, path):
    daily_token_dir = os.path.join(path, 'daily_tokens')
    today_date = datetime.datetime.now().strftime("%Y-%m-%d")
    filename = f"{today_date}.txt"
    ile_path = os.path.join(daily_token_dir, f"{today_date}.txt")
    acces_tokan = ""
    if os.path.exists(ile_path):
        with open(ile_path,mode="r") as file:
            acces_tokan = file.read()
        file.close()
        print("if block no new tokan")
    else:
        access_token = login_to_fyers(config)
        # print("final access tokan  "+access_token[1])
        with open(ile_path,mode="w") as file:
            file.write(access_token[1])
        file.close()
        print("else block new tokan")

    return acces_tokan








