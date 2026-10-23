import http.server
import socketserver
import urllib.parse
import json
import secrets
import webbrowser

# Salesforce is used as the concrete OAuth2/OIDC provider for this example
CLIENT_ID = 'YOUR_SALESFORCE_CLIENT_ID'
REDIRECT_URI = 'http://localhost:8080/callback'
SCOPE = 'openid profile email'
STATE = secrets.token_hex(16)

class OAuthHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        # If callback request
        if self.path.startswith('/callback'):
            parsed = urllib.parse.urlparse(self.path)
            query = urllib.parse.parse_qs(parsed.query)
            code = query.get('code', [''])[0]
            state_recv = query.get('state', [''])[0]
            if state_recv != STATE:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b'Invalid state parameter')
                return
            self.server.code = code
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'Login successful. You may close this window.')
        else:
            # Serve the authorization request page (simply redirect the user)
            self.send_response(302)
            self.send_header('Location', f'https://login.salesforce.com/services/oauth2/authorize?response_type=code&client_id={CLIENT_ID}&redirect_uri={urllib.parse.quote(REDIRECT_URI)}&scope={SCOPE}&state={STATE}')
            self.end_headers()


def start_oauth_login():
    """Start a local HTTP server to handle OAuth2 Authorization Code flow for Salesforce."""
    with socketserver.TCPServer(('', 8080), OAuthHandler) as httpd:
        print('Opening browser for Salesforce OAuth login...')
        webbrowser.open(f'https://login.salesforce.com/services/oauth2/authorize?response_type=code&client_id={CLIENT_ID}&redirect_uri={urllib.parse.quote(REDIRECT_URI)}&scope={SCOPE}&state={STATE}')
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print('OAuth server stopped')

if __name__ == '__main__':
    start_oauth_login()