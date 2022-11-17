# CS-Sender
scrapy extension for spider monitor web framework cralwer-studio


## Install
```
pip install cs-sender
```

## Usage 
Config following settings to settings.py of scrapy project
```
CS_BACKEND = http://localhost:8000
CS_API_TOKEN = '6452c52c4acee2044fe9d953467e6e45be1f367c'
EXTENSIONS = {
    'cs_sender.ScrapyMonitor': 802
}
```
