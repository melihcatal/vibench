import os
from requests import Request, Session

IBM_APPID_CLIENT_ID = os.getenv('IBM_APPID_CLIENT_ID')
IBM_APPID_CLIENT_SECRET = os.getenv('IBM_APPID_CLIENT_SECRET')

def start_oauth_login():
    authorization_endpoint = 'https://your-ibm-appid-instance.com/authorization'
    params = {
        'response_type': 'code',
        'client_id': IBM_APPID_CLIENT_ID,
        'redirect_uri': 'https://yourapp.com/callback',
        'scope': 'openid profile email'
    }
    session = Session()
    req = Request('GET', authorization_endpoint, params=params)
    prepared = session.prepare_request(req)
    return prepared.url