import os
import webbrowser
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

# Provider: Microsoft Entra OIDC (public client scenario)\n# SDK: msal (Microsoft Authentication Library)\nfrom msal import PublicClientApplication

# Configuration (environment variables)\nTENANT_ID = os.getenv('AZURE_TENANT_ID')
CLIENT_ID = os.getenv('AZURE_CLIENT_ID')
REDIRECT_URI = os.getenv('AZURE_REDIRECT_URI', 'http://localhost:5000/callback')

# Scopes needed for a federated login (openid + profile)\nSCOPES = ['openid', 'profile', 'email']

# PublicClientApplication – no client secret required\napp = PublicClientApplication(CLIENT_ID, authority=f'https://login.microsoftonline.com/{TENANT_ID}')

callback_result = {'code': None, 'verifier': None, 'state': None}

class PKCECallbackHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        query = urlparse(self.path).query
        params = parse_qs(query)
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        callback_result['code'] = params.get('code', [None])[0]
        callback_result['verifier'] = params.get('code_verifier', [None])[0]
        callback_result['state'] = params.get('state', [None])[0]
        self.wfile.write(b"<html><body><script>window.close();</script>Authentication callback received.</body></html>")

def start_callback_server(port=5000):
    server_address = ('', port)
    httpd = HTTPServer(server_address, PKCECallbackHandler)
    httpd.timeout = 5
    return httpd

def start_pkce_login():
    # Generate PKCE code challenge and verifier\n    verifier, challenge = app._build_pkce_codes()  # internal helper; in production use a dedicated pkce lib if needed\n    # Build authorization URL with PKCE parameters\n    auth_url = app.create_auth_url(
        scopes=SCOPES,
        redirect_uri=REDIRECT_URI,
        state='post_login',          # CSRF protection token\n        code_challenge=challenge,
        code_challenge_method='S256',  # recommended\n        prompt='login'                # force login page\n    )\n    print('Open the following URL in your browser and complete login:')
    print(auth_url)\n    # Launch the callback server in a background thread\n    server = start_callback_server()
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True
    server_thread.start()\n    webbrowser.open(auth_url)\n    # Wait for the callback\n    while callback_result['code'] is None:\n        threading.Event().wait(0.5)\n    # Shut down server\n    server.shutdown()
    server.server_close()\n    print('Received authorization code and verifier.')\n    # Exchange code for token – PKCE flow uses the same endpoint as auth code flow\n    try:
        token_response = app.acquire_token_by_authorization_code(
            code=callback_result['code'],
            scopes=SCOPES,
            redirect_uri=REDIRECT_URI,
            code_verifier=callback_result['verifier']
        )\n        if 'access_token' not in token_response:
            raise ValueError('Access token missing')\n        print('Token exchange succeeded. Token:', token_response['access_token'])\n    except Exception as e:
        print('Token exchange failed:', e)\n\nif __name__ == '__main__':
    start_pkce_login()
