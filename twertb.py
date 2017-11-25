#!/usr/bin/env python3

# -*- coding: utf-8 -*-

# TransferWise Exchange Rate Telegram Bot
# https://github.com/Amet13/twertb

from urllib.request import urlopen, Request
import re, json

tw_domain = 'https://transferwise.com'
tw_url = 'https://transferwise.com/tools/exchange-rate-alerts/'
tw_header = 'Mozilla/5.0'
tw_api_url = 'https://api.transferwise.com/v1/rates'
output_json_file = 'currencies.json'

def getJsLink():
	url = Request(tw_url)
	url.add_header('User-Agent', tw_header)
	text = urlopen(url).read().decode('utf-8')
	jslink = re.search('/tools/exchange-rate-alerts/static/js/main.*.js', text).group(0)
	return jslink

def getToken():
	#tw_js_url = getJsLink()
	url = Request(tw_domain + getJsLink())
	url.add_header('User-Agent', tw_header)
	text = urlopen(url).read().decode('utf-8')
	token = re.search('RATE_API_TOKEN:\"(\S*)\",', text).group(1)
	return token

# Get Json and write to file
def getJsonData():
	url = Request(tw_api_url)
	#token = getToken()
	url.add_header('authorization', 'Basic ' + getToken())
	text = urlopen(url).read().decode('utf-8')
	parsed = json.loads(text)
	with open(output_json_file, 'w') as file:
		file.write(json.dumps(parsed, indent=4, sort_keys=True))

getJsonData()
