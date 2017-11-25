#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from urllib.request import urlopen, Request
from urllib.parse import urlencode
import re
import json
import argparse
import os.path

tw_domain = 'https://transferwise.com'
tw_url = tw_domain + '/tools/exchange-rate-alerts/'
tw_header = 'Mozilla/5.0'
tw_api_url = 'https://api.transferwise.com/v1/rates'
output_json_file = 'misc/currencies.json'

def checkFile():
    return os.path.exists(output_json_file)

def parseArguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--update', dest='UPDATE', action='store_true', help='update currency rates')
    parser.add_argument('-s', '--source', dest='SOURCE', required=True, help='source currency')
    parser.add_argument('-t', '--target', dest='TARGET', required=True, help='target currency')
    parser.add_argument('--token', dest='TG_TOKEN', default='', help='telegram token')
    parser.add_argument('--id', dest='TG_ID', default='', help='telegram id')
    namespace = parser.parse_args()

    global source, target, update_currency, tg_token, tg_id
    update_currency = namespace.UPDATE
    source = namespace.SOURCE
    target = namespace.TARGET
    tg_token = namespace.TG_TOKEN
    tg_id = namespace.TG_ID

    if source == target:
        print('You can\'t convert {0} to same currency {1}'.format(source, target))

def getJsLink():
    url = Request(tw_url)
    url.add_header('User-Agent', tw_header)
    text = urlopen(url).read().decode('utf-8')
    jslink = re.search('/tools/exchange-rate-alerts/static/js/main.*.js', text).group(0)
    return jslink

def getToken():
    url = Request(tw_domain + getJsLink())
    url.add_header('User-Agent', tw_header)
    text = urlopen(url).read().decode('utf-8')
    token = re.search('RATE_API_TOKEN:\"(\S*)\",', text).group(1)
    return token

def getJsonData():
    url = Request(tw_api_url)
    url.add_header('authorization', 'Basic ' + getToken())
    text = urlopen(url).read().decode('utf-8')
    parsed = json.loads(text)
    with open(output_json_file, 'w') as file:
        file.write(json.dumps(parsed, indent=4, sort_keys=True))
    print('Currency database updated')

def getCurrency():
    currency_data = json.loads(open(output_json_file).read())
    for each in currency_data:
        if each['source'] == source and each['target'] == target:
            global exchange_res
            exchange_res = '1{0} = {1}{2} at {3}'.format(source, each['rate'], target, each['time'])
            print(exchange_res)

def sendToTelegram():
    tg_url = 'https://api.telegram.org/bot'
    tg_full = '{0}{1}/sendMessage'.format(tg_url, tg_token)
    tg_params = urlencode({'chat_id': tg_id, 'text': exchange_res}).encode('utf-8')
    urlopen(tg_full, tg_params)
    print('Message sent to Telegram')

def main():
    if checkFile() is False: getJsonData()
    parseArguments()
    if update_currency is True: getJsonData()
    getCurrency()
    if tg_token != '' and tg_id != '': sendToTelegram()

if __name__ == '__main__':
    main()
