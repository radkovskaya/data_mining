import requests
import json
git_hub_url = 'https://api.github.com/users/'
user_name = 'radkovskaya'
response = requests.get(f'{git_hub_url}{user_name}/repos')
data = json.loads(response.text)
data_name = [x['name'] for x in data]
f = open('data.json', 'w')
f.write(str(data_name))
f.close()