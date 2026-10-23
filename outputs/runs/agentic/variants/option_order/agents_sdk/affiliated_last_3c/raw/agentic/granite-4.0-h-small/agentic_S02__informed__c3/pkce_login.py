import os
import secrets
import urllib.parse
import http.server
import socketserver
from auth0 import AuthenticationClient

# Configurable values - set env vars or replace with constants
AUTH0_DOMAIN = os.getenv('AUTH0_DOMAIN', 'your-auth0-domain.auth0.com')
AUTH0_CLIENT_ID = os.getenv('AUTH0_CLIENT_ID', 'your-auth0-client-id')
REDIRECT_URI = 'http://localhost:5001/oauth_pkce_callback'
SCOPE = 'openid profile email'

# Initialize Auth0 client (used for token exchange)
auth_client = AuthenticationClient(
    domain=AUTH0_DOMAIN,
    client_id=AUTH0_CLIENT_ID,
)

# PKCE utilities
verifier = secrets.token_urlsafe(32)
challenge = auth_client.secret_code(verifier)  # S256 method

class PKCEHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        # Authorization request
        if self.path == '/authorize_pkce':
            params = {
                'response_type': 'code',
                'client_id': AUTH0_CLIENT_ID,
                'redirect_uri': REDIRECT_URI,
                'scope': SCOPE,
                'code_challenge': challenge,
                'code_challenge_method': 'S256',
                'state': secrets.token_hex(16),
            }
            auth_url = f"https://{AUTH0_DOMAIN}/authorize?" + urllib.parse.urlencode(params)
            self.send_response(302)
            self.send_header('Location', auth_url)
            self.end_headers()
            self.wfile.write(b'Redirecting to Auth0 authorization endpoint...')
            return
        # Callback handling (exchange code for tokens)
        if self.path.startswith('/oauth_pkce_callback'):
            query = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
            code = query.get('code', [None])[0]
            state = query.get('state', [None])[0]
            if not code or not state:
                self.send_response(400)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self.wfile.write(b'Invalid callback parameters.')
                return
            # Exchange for tokens using Auth0 SDK (PKCE flow)
            token_res = auth_client.oauth.get_tokens_by_code(
                code=code,
                redirect_uri=REDIRECT_URI,
            )
            if not token_res.get('access_token'):
                self.send_response(500)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self.wfile.write(b'Token exchange failed.')
                return
            # Echo back tokens (in production store securely)
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(token_res.encode('utf-8'))
            return
        # Fallback / index
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b'PKCE login server. Visit /authorize_pkce to start.')

PORT = 5001
Handler = PKCEHandler
with socketserver.TCPServer(("localhost", PORT), Handler) as httpd:
    print(f"PKCE login service listening on http://localhost:{PORT}")
    # Simple blocking serve for demo purposes
    httpd.serve_forever()
