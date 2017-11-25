#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from urllib.request import urlopen, Request
from urllib.parse import urlencode
import re, json, argparse, os.path

tw_domain = 'https://transferwise.com'
tw_url = tw_domain + '/tools/exchange-rate-alerts/'
tw_header = 'Mozilla/5.0'
tw_api_url = 'https://api.transferwise.com/v1/rates'
output_json_file = 'misc/currencies.json'

def checkFile():
    return os.path.exists(output_json_file)

def parseArguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--source', dest='SOURCE', required=True, help='source currency')
    parser.add_argument('-t', '--target', dest='TARGET', required=True, help='target currency')
    parser.add_argument('-g', '--get-data', dest='GETDATA', required=True, help='set \'yes\' if need to update database?')
    parser.add_argument('--token', dest='TGTOKEN', default='', help='set telegram token')
    parser.add_argument('--id', dest='TGID', default='', help='set telegram  id')
    namespace = parser.parse_args()

    global source, target, get_data, tg_token, tg_id
    source = namespace.SOURCE
    target = namespace.TARGET
    update_currency = namespace.GETDATA

    if source == target:
        print('You can\'t convert {0} to same currency {1}'.format(source, target))
    if update_currency == 'yes':
        get_data = True
    else:
        get_data = False

    #print(namespace.TGTOKENID[0])
    try:
        tg_token = namespace.TGTOKEN
        tg_id = namespace.TGID
    except(IndexError):
        tg_token = ''
        tg_id = ''

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

def getCurrency():
    currency_data = json.loads(open(output_json_file).read())
    for each in currency_data:
        if each['source'] == source and each['target'] == target:
            global exchange_result
            exchange_result = '1{0} = {1}{2} at {3}'.format(source, each['rate'], target, each['time'])
            print(exchange_result)

def sendToTelegram():
    tg_url = 'https://api.telegram.org/bot'
    tg_full = '{0}{1}/sendMessage'.format(tg_url, tg_token)
    tg_params = urlencode({'chat_id': tg_id, 'text': exchange_result}).encode('utf-8')
    urlopen(tg_full, tg_params)
    print('Message sent to Telegram')

# Check if currency.json exists
if checkFile() is False:
    getJsonData()

# Parse arguments
parseArguments()

# If need to update currencies do it
if get_data is True:
    getJsonData()

# Get currency
getCurrency()

if tg_token != '' and tg_id != '':
    sendToTelegram()
