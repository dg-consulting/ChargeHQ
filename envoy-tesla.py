import urllib.request,json,requests
from config import *
from socket import timeout
from urllib.error import HTTPError, URLError

source = 'https://your_enjoy_ip/production.json'
endPoint = 'https://api.chargehq.net/api/public/push-solar-data'
apiKey = '440e...30accca'

# REPLACE ITEMS BELOW 
user='your_mail'
password='PWD'
envoy_serial='serial_number_envoy'
# DO NOT CHANGE ANYTHING BELOW

data = {'user[email]': user, 'user[password]': password}
response = requests.post('https://enlighten.enphaseenergy.com/login/login.json?',data=data)
response_data = json.loads(response.text)
data = {'session_id': response_data['session_id'], 'serial_num': envoy_serial, 'username':user}
response = requests.post('https://entrez.enphaseenergy.com/tokens', json=data)
token_raw = response.text

headers = {
        'Authorization': 'Bearer' + token_raw,
        'Content-Type': 'application/json'
    }

headers = {'Authorization': f'Bearer {token_raw}'}
reponses_envoy = requests.get(source, headers=headers, verify=False)
reponses_envoy = reponses_envoy.json()

# Massage Envoy json into ChargeHQ compatible json
consumption = round(reponses_envoy['consumption'][0]['wNow'] / 1000,2)
production = round(reponses_envoy['production'][0]['wNow'] / 1000,2)
grid = round(production - consumption,2)

if grid <0:
    grid = abs(grid) # Invert grid value from Envoy value to keep ChargeHQ happy
else:
    grid = -abs(grid) # Invert grid value from Envoy value to keep ChargeHQ happy

# create new json

jsondata = {}
jsondata['apiKey'] = apiKey
jsondata['siteMeters'] = {}
jsondata['siteMeters']['production_kw'] = production
jsondata['siteMeters']['net_import_kw'] = grid
jsondata['siteMeters']['consumption_kw'] = consumption 
json_dump = json.dumps(jsondata)
    
# POST json to ChargeHQ

header = {'Content-type': 'application/json', 'Accept': 'text/plain'}
r = requests.post(endPoint, data=json_dump, headers=header)
#print(f"Status Code: {r.status_code}, Response: {r.json()}")
print (r)
