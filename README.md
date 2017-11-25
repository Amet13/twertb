# TransferWise Exchange Rate Telegram Bot

[![TravisCI](https://travis-ci.org/Amet13/twertb.svg?branch=master)](https://travis-ci.org/Amet13/twertb/)
[![License](https://img.shields.io/badge/license-GNU_GPLv3-red.svg)](https://www.gnu.org/licenses/gpl-3.0.html)

Withdraw your money from TransferWise account with a favorable exchange rate

## Usage

### Clone repo and get help:

```
$ git clone https://github.com/Amet13/twertb
$ cd twertb/
$ ./twertb.py -h
usage: twertb.py [-h] [-u] -s SOURCE -t TARGET [--token TG_TOKEN] [--id TG_ID]

optional arguments:
  -h, --help            show this help message and exit
  -u, --update          update currency rates
  -s SOURCE, --source SOURCE
                        source currency
  -t TARGET, --target TARGET
                        target currency
  --token TG_TOKEN      telegram token
  --id TG_ID            telegram id
```

### Get last currency database and get exchange rate for `EUR/USD`:

```
$ ./twertb.py -s EUR -t USD -u
Currency database updated
1EUR = 1.193USD at 2017-11-25T11:24:53+0000
```

### Get exchange rate for `GBP/RUB` without updating database:

```
$ ./twertb.py -s GBP -t RUB
1GBP = 77.88126RUB at 2017-11-25T11:24:57+0000
```

## Send exchange rates to Telegram

* go to [@BotFather](https://t.me/BotFather) and create `/newbot`, for example `TWERTB_bot`
* then you have token like `111111111:ABCDE...`
* after go to [@MyTelegramID_bot](https://t.me/MyTelegramID_bot) and `/start` it
* then you have your telegram ID like `123456789`

### Now you can run script with your token and ID:

```
TOKEN='111111111:ABCDE'
ID='123456789'
$ ./twertb.py -s EUR -t USD --token ${TOKEN} --id ${ID}
1EUR = 1.193USD at 2017-11-25T12:04:46+0000
Message sent to Telegram
```

### Screenshot

![](https://raw.githubusercontent.com/Amet13/twertb/master/misc/screenshot.jpg)

## Autoupdate currencies

```
$ crontab -e
*/5 * * * * cd /path/to/twertb/ ; ./twertb.py -s EUR -t USD -u --token ${TOKEN} --id ${ID} &> /dev/null
```

## Serverless usage via GitHub and TravisCI

Just enable daily Cron Job in TravisCI settings and get exchange rate every day.

![](https://raw.githubusercontent.com/Amet13/twertb/master/misc/cronjob.png)
