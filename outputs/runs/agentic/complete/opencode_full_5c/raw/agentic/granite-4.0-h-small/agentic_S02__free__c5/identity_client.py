import os
from typing import Dict, Any

# Provider configuration: Okta example
OKTA_DOMAIN = os.getenv('OKTA_DOMAIN', 'dev-12345.okta.com')
OKTA_CLIENT_ID = os.getenv('OKTA_CLIENT_ID')
OKTA_REDIRECT_URI = os.getenv('OKTA_REDIRECT_URI', 'http://localhost:8080/callback')


class IdentityClient:
    def __init__(self):
        self.token = None

    def start_oauth_user_agent_flow(self) -> str:
        import webbrowser
        import http.server
        import socketserver
        from urllib.parse import urlencode, urlparse

        auth_url = f'https://{OKTA_DOMAIN}/oauth2/default/v1/authorize?' + urlencode({
            'client_id': OKTA_CLIENT_ID,
            'redirect_uri': OKTA_REDIRECT_URI,
            'response_type': 'code',
            'scope': 'openid profile email',
            'state': 'okta-state',
        })
        print('Opening browser to:', auth_url)
        webbrowser.open(auth_url)

        class Handler(http.server.SimpleHTTPRequestHandler):
            def do_GET(self):
                if self.path.startswith('/callback'):
                    query = urlparse(self.path).query
                    params = dict(param.split('=') for param in query.split('&') if param)
                    code = params.get('code')
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    self.wfile.write(b'<html><body><script>window.close();</script>You may close this window.</body></html>')
                    raise socketserver.socket.error  # break server loop
                else:
                    self.send_error(404)

        with socketserver.TCPServer(('', 8080), Handler) as httpd:
            httpd.handle_request()  # runs once
        return code  # noqa: F821

    def exchange_code(self, code: str) -> Dict[str, Any]:
        import requests
        TOKEN_ENDPOINT = f'https://{OKTA_DOMAIN}/oauth2/default/v1/token'
        resp = requests.post(TOKEN_ENDPOINT, data={
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': OKTA_REDIRECT_URI,
            'client_id': OKTA_CLIENT_ID,
        })
        resp.raise_for_status()
        self.token = resp.json()
        return self.token

    def get_userinfo(self) -> Dict[str, Any]:
        if not self.token:
            raise RuntimeError('Token not set')
        resp = requests.get('https://okta-example.com/oauth2/default/v1/userinfo',
                            headers={'Authorization': f'Bearer {self.token["access_token"]}')
        resp.raise_for_status()
        return resp.json()
