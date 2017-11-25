# TransferWise Exchange Rate Telegram Bot

Withdraw your money from Transferwise account with a favorable exchange rate.

## Usage

Clone repo:
```bash
git clone https://github.com/Amet13/twertb
```

Get help:
```bash
python3 twertb/ -h
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

Get last currency database to json file and check currency for `EUR/USD`:
```bash
python3 twertb -s EUR -t USD -g yes
1EUR = 1.193USD at 2017-11-25T11:24:53+0000
```

Check currency for `GBP/RUB` without updating database:
```bash
python3 twertb -s GBP -t RUB -g no
1GBP = 77.88126RUB at 2017-11-25T11:24:57+0000
```

## TODO

* Telegram bot
* TravisCI cron autoupdate database
* Free hosting for it
