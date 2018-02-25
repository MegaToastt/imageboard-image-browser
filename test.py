import requests
from datetime import datetime

s = requests.Session()

url = 'https://a.4cdn.org/boards.json'
timestamp = datetime.utcnow()
print(timestamp.strftime('%a, %d %b %Y %H:%M:%S GMT'))
#s.headers.update({'if-modified-since': timestamp.strftime('%a, %d %b %Y %H:%M:%S GMT')})
#s.headers.update({'If-Modified-Since': 'Sun, 25 Feb 2018 00:00:00 GMT'})

test = s.get(url, headers={'If-Modified-Since': 'Sun, 25 Feb 2018 00:00:00 GMT'})
print(test.status_code)
print(test.headers)
