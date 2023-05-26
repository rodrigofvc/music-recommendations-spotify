import requests

def request_token():
    token_url = "https://accounts.spotify.com/api/token"
    # Personal keys
    client_id = ''
    client_secret = ''
    data = {'grant_type': 'client_credentials', 'client_id': client_id, 'client_secret': client_secret}
    r = requests.post(token_url, data=data)
    d = r.json()
    print (d['access_token'])
    return d['access_token']

#request_token()
