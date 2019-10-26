import requests
import json
fm_url = 'http://ws.audioscrobbler.com/2.0/'
method = 'artist.getinfo'
artist = 'Cher'
api_key = '322714fe82ba22e2b30660a5d8dd6ebc'
format = 'json'
req = requests.get(f'{fm_url}?method={method}&artist={artist}&api_key={api_key}&format={format}')
print(req.url)
data = json.loads(req.text)
print(data)

