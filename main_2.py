import pandas as pd
import os
from utils.read_json import read_json_file
from fyers_api_algo.fyers_app_login import get_access_tokan_final


def main():
    json_file_path = 'config.json'  # Path to the JSON file in the project directory

    path = os.path.dirname(os.path.abspath(__file__))
    # print(os.getcwd())
    config = read_json_file(json_file_path)

    # login api
    access_token = get_access_tokan_final(config, path)

    # profile api
    client_id = f"{config['APP_ID']}-{config['APP_TYPE']}"

    return [access_token, client_id]

if __name__ == "__main__":
    main()