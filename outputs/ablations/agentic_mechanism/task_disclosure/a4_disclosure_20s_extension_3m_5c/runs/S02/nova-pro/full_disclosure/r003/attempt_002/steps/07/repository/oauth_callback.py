import requests

AUTH0_DOMAIN = 'your-auth0-domain.auth0.com'
CLIENT_ID = 'your-client-id'
CLIENT_SECRET = 'your-client-secret'

def exchange_code_for_tokens(code):
    url = f'https://{AUTH0_DOMAIN}/oauth/token'
    payload = {
        'grant_type': 'authorization_code',
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'code': code,
        'redirect_uri': 'https://your-app.com/callback'
    }
    response = requests.post(url, data=payload)
    response.raise_for_status()
    return response.json()

def handle_callback(request):
    code = request.args.get('code')
    if code:
        tokens = exchange_code_for_tokens(code)
        return tokens
    else:
        return {'error': 'No code provided'}