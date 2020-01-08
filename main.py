import requests
import argparse
import json
import os
from dotenv import load_dotenv, find_dotenv
load_dotenv()

URL = 'https://api-ssl.bitly.com/v4/user'
API_URL = 'https://api-ssl.bitly.com/v4/bitlinks'


def create_argument():
    parser = argparse.ArgumentParser(description='Ссылка для сокращения')
    parser.add_argument('link', type=str, help='Input link for conversion')
    args = parser.parse_args()
    return args.link


def shorten_link(user_link_input, api_token, headers):
    headers = {'Authorization': api_token}
    response_bitlinks = requests.post(API_URL,
                                      json={'long_url': user_link_input},                                            headers=headers)
    bitlink = response_bitlinks.json()['id']
    return bitlink


def count_clicks(short_link, api_token, headers):
    payload = {"units": -1,
               "unit": "day"
               }
    sum_of_clicks = requests.get('https://api-ssl.bitly.com/v4/bitlinks/{}/clicks/summary'.format(short_link),                                 params=payload, 
                                 headers=headers)
    return sum_of_clicks.json()['total_clicks']


if __name__ == "__main__":
    load_dotenv(find_dotenv())
    api_token = os.getenv("BITLY_TOKEN")
    headers = {'Authorization': api_token}
    user_link_input = create_argument()
    if user_link_input.startswith("bit.ly/"):
        short_link = user_link_input
        print("По вашей ссылке прошли: ", count_clicks(short_link, api_token, headers), "раз")
    elif user_link_input.startswith("http://") or ("https://"):
        long_url = user_link_input
        print("Ваша короткая ссылка: ", shorten_link(user_link_input, api_token, headers))
    else:
        print("Попробуйте еще раз, нерабочая ссылка")
    try:
        user_link_input = create_argument()
    except requests.exceptions.HTTPError:
        print("Выход")
    except Exception as exc:
        print("Вы ввели неверную ссылку")
        
