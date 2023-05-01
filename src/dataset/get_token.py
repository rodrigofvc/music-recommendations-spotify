import requests

token_url = "https://accounts.spotify.com/api/token"
# Personal keys
client_id = 'INSERTA TU CLIENT ID'
client_secret = 'INSERTA TU CLIENT SECRET'
data = {'grant_type': 'client_credentials', 'client_id': client_id, 'client_secret': client_secret}

r = requests.post(token_url, data=data)
print (r.text)
