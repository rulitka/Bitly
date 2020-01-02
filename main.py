from dotenv import load_dotenv, find_dotenv
import requests
load_dotenv(find_dotenv())
import argparse
import json
import os

URL = 'https://api-ssl.bitly.com/v4/user'
API_URL = 'https://api-ssl.bitly.com/v4/bitlinks'
BITLY_TOKEN = os.getenv("TOKEN")
HEADERS = {'Authorization': BITLY_TOKEN}

def createParser():
  parser = argparse.ArgumentParser(description='Ссылка для сокращения')
  parser.add_argument('link', type=str, help='Input link for conversion')
 
  return parser

def shorten_link(user_input): 
  response_bitlinks = requests.post(API_URL, json={'long_url': user_input}, headers = HEADERS)
  bitlink = response_bitlinks.json()['id']
  return bitlink
  
def count_clicks(short_link):
  payload = {
  "units": -1,
  "unit": "day"}
  sum_of_clicks = requests.get('https://api-ssl.bitly.com/v4/bitlinks/{}/clicks/summary'.format(short_link), params=payload, headers = HEADERS)
  return sum_of_clicks.json()['total_clicks']

def main():
  parser = createParser()
  user_input = parser.parse_args()
  if user_input.startswith("bit.ly/"):
    short_link = user_input 
    print ("По вашей ссылке прошли: ",count_clicks(short_link), "раз")          
  elif user_input.startswith("http://") or ("https://"):
    long_url = user_input
    print ("Ваша короткая ссылка: ", shorten_link(user_input)) 
  else:
    print ("Попробуйте еще раз, нерабочая ссылка") 
 

if __name__== "__main__":
  try:
    main()
  except requests.exceptions.HTTPError:
    print("Выход")
  except Exception as exc:
    print ("Вы ввели неверную ссылку") 







