# TransferWise Exchange Rate Telegram Bot

Withdraw your money from Transferwise account with a favorable exchange rate.

## Usage

### Clone repo and get help:

```
$ git clone https://github.com/Amet13/twertb
$ python3 twertb/ -h
usage: [-h] -s SOURCE -t TARGET -g GETDATA

optional arguments:
  -h, --help            show this help message and exit
  -s SOURCE, --source SOURCE
                        source currency
  -t TARGET, --target TARGET
                        target currency
  -g GETDATA, --get-data GETDATA
                        set 'yes' if need to update database?
```

### Get last currency database and get exchange rate for `EUR/USD`:

```
$ python3 twertb -s EUR -t USD -g yes
Currency database updated
1EUR = 1.193USD at 2017-11-25T11:24:53+0000
```

### Get exchange rate for `GBP/RUB` without updating database:

```
$ python3 twertb -s GBP -t RUB -g no
1GBP = 77.88126RUB at 2017-11-25T11:24:57+0000
```

## Send exchange rates to Telegram

* go to [@BotFather](https://t.me/BotFather) and create `/newbot`, for example `TWERTB_bot`
* then you have token like `111111111:ABCDE...`
* after go to [@MyTelegramID_bot](https://t.me/MyTelegramID_bot) and `/start` it
* then you have your telegram ID like `123456789`

### Now you can run script with your token and ID:

```
$ python3 twertb -s EUR -t USD -g no --token 111111111:ABCDE --id 123456789
1EUR = 1.193USD at 2017-11-25T12:04:46+0000
Message sent to Telegram
```

### Screenshot

![](https://raw.githubusercontent.com/Amet13/twertb/master/misc/screenshot.jpg)

## Autoupdate databases

```
$ crontab -e
*/5 * * * * cd /path/to/twertb/ ; /usr/bin/python3 __main__.py -s EUR -t USD -g yes --token 111111111:ABCDE --id 123456789 &> /dev/null
```

## TODO

* Telegram bot (client/server)
* TravisCI cron autoupdate database
* Free hosting for it
