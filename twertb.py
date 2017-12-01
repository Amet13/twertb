#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from urllib.request import urlopen, Request
from urllib.parse import urlencode
import urllib
import re
import json
import argparse
import os.path
import datetime
import sys

tw_domain = 'https://transferwise.com'
tw_url = tw_domain + '/tools/exchange-rate-alerts/'
tw_header = 'Mozilla/5.0'
tw_api_url = 'https://api.transferwise.com/v1/rates'
json_file_name = '/misc/currencies.json'
js_file_name = '/tools/exchange-rate-alerts/static/js/main.*.js'
output_json_file = os.path.dirname(os.path.realpath(__file__)) + json_file_name


def checkFile():
    return os.path.exists(output_json_file)


def parseArguments():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-u', '--update',
        dest='UPDATE',
        action='store_true',
        help='update currency rates'
    )
    parser.add_argument(
        '-e', '--exchange',
        dest='EXCHANGE',
        metavar=('SOURCE', 'TARGET'),
        nargs=2,
        help='currencies for exchange'
    )
    parser.add_argument(
        '-a', '--alert',
        dest='ALERT',
        help='alert when 1 SOURCE goes above X TARGET'
    )
    parser.add_argument(
        '-p', '--print',
        dest='CURRENCIES',
        action='store_true',
        help='print available currencies'
    )
    parser.add_argument(
        '-t', '--token',
        dest='TG_TOKEN',
        help='telegram token'
    )
    parser.add_argument(
        '-i', '--id',
        dest='TG_ID',
        help='telegram id'
    )

    namespace = parser.parse_args()
    global update_currency, source, target, alert, currencies, tg_token, tg_id
    try:
        source = namespace.EXCHANGE[0]
        target = namespace.EXCHANGE[1]
    except(TypeError):
        source = None
        target = None

    update_currency = namespace.UPDATE
    alert = namespace.ALERT
    currencies = namespace.CURRENCIES
    tg_token = namespace.TG_TOKEN
    tg_id = namespace.TG_ID

    if source is not None and target is not None and source == target:
        print('You can\'t convert {0} to same currency'.format(source))
        sys.exit(1)

    if update_currency is False and alert is not None:
        print('You can\'t use -a (--alert) argument without -u (--update)')
        sys.exit(1)

    if currencies is True:
        print('Available currencies:')
        getCurrenciesList()
        sys.exit(0)


def getJsLink():
    url = Request(tw_url)
    url.add_header('User-Agent', tw_header)
    text = urlopen(url).read().decode('utf-8')
    jslink = re.search(js_file_name, text).group(0)
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
    print(
        'Currency database updated ({0})'
        .format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    )


def getCurrency():
    currency_data = json.loads(open(output_json_file).read())
    for each in currency_data:
        if each['source'] == source and each['target'] == target:
            global ex_res, ex_rate
            ex_rate = each['rate']
            ex_res = '1 {0} = {1} {2}'.format(source, ex_rate, target)
            print(ex_res)


def sendToTelegram():
    tg_url = 'https://api.telegram.org/bot'
    tg_full = '{0}{1}/sendMessage'.format(tg_url, tg_token)
    tg_params = urlencode({'chat_id': tg_id, 'text': ex_res}).encode('utf-8')
    try:
        urlopen(tg_full, tg_params)
        print('Message sent to Telegram')
    except(urllib.error.HTTPError):
        print('Message not sent to Telegram, check your TOKEN and ID')
        sys.exit(1)


def checkAlert():
    if alert is not None and float(alert) < float(ex_rate):
        print('{0} < {1}'.format(float(alert), float(ex_rate)))
        if tg_token and tg_id:
            sendToTelegram()


def getCurrenciesList():
    url = Request(tw_domain + getJsLink())
    url.add_header('User-Agent', tw_header)
    text = urlopen(url).read().decode('utf-8')
    currencies = re.findall('code:\"[A-Z]*\",country:\"\w*.\w*.\w*\"', text)
    for countrycode in currencies:
        data = re.findall('"[a-zA-Z]*.\w*.\w*\"', countrycode)
        print(': '.join(data).replace("\"", ""))


def main():
    parseArguments()
    if checkFile() is False or update_currency is True:
        getJsonData()
    getCurrency()
    if tg_token and tg_id and alert is None:
        sendToTelegram()
    if alert:
        checkAlert()
    sys.exit(0)


main()
