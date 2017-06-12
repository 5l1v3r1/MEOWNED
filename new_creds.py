import requests
import re

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
    'Referer': 'https://twitter.com/',
    'Accept-Encoding': 'gzip,deflate',
    'Host': 'twitter.com',
    'Connection': 'Keep-Alive'
}

url = "https://twitter.com/search?f=tweets&q=%23NEW_CREDENTIALS%20%230fb8539d64f0899d2b0552fd2dde5328f5494d3a1bbad3dbcdbeafbb73c1fae4"

response = requests.get(url, headers=headers)
content = response.text.encode('utf-8').strip()

pattern = re.compile(r'(https:\/\/pbs\.twimg\.com\/media\/.*\.png)')

for (image_url) in re.findall(pattern, content):
    print image_url