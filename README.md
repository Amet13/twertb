# TransferWise Exchange Rate Telegram Bot

[![TravisCI](https://travis-ci.org/Amet13/twertb.svg?branch=master)](https://travis-ci.org/Amet13/twertb/)
[![License](https://img.shields.io/badge/license-GNU_GPLv3-red.svg)](https://www.gnu.org/licenses/gpl-3.0.html)
[![Python](https://img.shields.io/badge/python-3.6-blue.svg)](https://github.com/Amet13/twertb/blob/master/.travis.yml)

Get a Telegram message and withdraw money from TransferWise account with favorable exchange rate

## Usage

**Clone repo and get help:**
```
$ git clone https://github.com/Amet13/twertb
$ python3 twertb/ -h
usage: [-h] [-u] [-e SOURCE TARGET] [-a ALERT] [-p] [-t TG_TOKEN] [-i TG_ID]

optional arguments:
  -h, --help            show this help message and exit
  -u, --update          update currency rates
  -e SOURCE TARGET, --exchange SOURCE TARGET
                        source and target currency for exchange
  -a ALERT, --alert ALERT
                        alert when 1 SOURCE goes above X TARGET
  -p, --print           print available currencies
  -t TG_TOKEN, --token TG_TOKEN
                        telegram token
  -i TG_ID, --id TG_ID  telegram id
```

**Get last currency database and get exchange rate for `EUR/USD`:**
```
$ python3 twertb/ -e EUR USD -u
Currency database updated (2017-12-01 13:49:58)
1 EUR = 1.189 USD
```

**Get exchange rate for `GBP/RUB` without updating database:**
```
$ python3 twertb/ -e GBP RUB
1 GBP = 79.14778 RUB
```

**Show available currencies (for example grep by A end E):**
```
$ python3 twertb/ -p | egrep '^A|^E'
Available currencies:
AED: United Arabian Emirates
AUD: Australia
EUR: Europe
AFN: Afghanistan
ARS: Argentina
EGP: Egypt
ETB: Ethiopia
```

## Send exchange rates message to Telegram

1. Go to [@BotFather](https://t.me/BotFather) and create `/newbot` (for example `TWERTB_bot`)
2. You will receive a token like `111111111:ABCDE`, remember it
3. Then go to [@MyTelegramID_bot](https://t.me/MyTelegramID_bot) and `/start` it
4. You will receive your Telegram ID like `123456789`, also remember it

## Run script with your token and ID

```
TOKEN='111111111:ABCDE'
ID='123456789'
$ python3 twertb/ -e EUR RUB -t $TOKEN -i $ID
1 EUR = 69.66249 RUB
Message sent to Telegram
```

![](https://raw.githubusercontent.com/Amet13/twertb/master/misc/message.jpg)

## Autoupdate currencies

Add to cron a job for updating a currencies database (for example every two hours):
```
$ crontab -e
* */2 * * * /usr/bin/python3 /path/to/twertb/ -u &> /dev/null
```

## Get a Telegram message when exchange rate is favorable

Add to cron task for every 10 minutes checks and get alert when `1 EUR > 70 RUB`:
```
$ crontab -e
*/10 * * * * /usr/bin/python3 /path/to/twertb/ -e EUR RUB -u -a 70 -t $TOKEN -i $ID &> /dev/null
```

## Serverless bot usage via GitHub and TravisCI

Just enable daily Cron Job in TravisCI settings and get exchange rate every day.

![](https://raw.githubusercontent.com/Amet13/twertb/master/misc/cronjob.png)
