import os
import urllib.parse
import http.server
import socketserver
from auth0 import AuthenticationClient

# Configurable values – set environment variables or replace with constants
AUTH0_DOMAIN = os.getenv('AUTH0_DOMAIN', 'your-auth0-domain.auth0.com')
AUTH0_CLIENT_ID = os.getenv('AUTH0_CLIENT_ID', 'your-auth0-client-id')
REDIRECT_URI = 'http://localhost:5000/oauth_callback'
SCOPE = 'openid profile email'

# Initialize Auth0 client (uses Management API token if needed for later steps)
auth_client = AuthenticationClient(
    domain=AUTH0_DOMAIN,
    client_id=AUTH0_CLIENT_ID,
)

# State and PKCE utilities (kept simple for demo)
import secrets
state = secrets.token_hex(16)
verifier = secrets.token_urlsafe(32)
challenge = Auth0Client.secret_code(verifier)

class AuthHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        # If this is the callback path, handle token exchange (defer to oauth_callback.py)
        if self.path.startswith('/oauth_callback'):
            self.server.future_response = self.path  # simple bridge for demo
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b"<script>window.close();</script>Thank you!")
            return
        # Authorization request – start flow
        params = {
            'response_type': 'code',
            'client_id': AUTH0_CLIENT_ID,
            'redirect_uri': REDIRECT_URI,
            'scope': SCOPE,
            'state': state,
            'code_challenge': challenge,
            'code_challenge_method': 'S256',
        }
        auth_url = f"https://{AUTH0_DOMAIN}/authorize?" + urllib.parse.urlencode(params)
        self.send_response(302)
        self.send_header('Location', auth_url)
        self.end_headers()
        self.wfile.write(b"Redirecting to authorization URL...")

PORT = 5000
Handler = AuthHandler
with socketserver.TCPServer(("localhost", PORT), Handler) as httpd:
    httpd.future_response = None  # placeholder for callback capture
    print(f"OAuth login server listening on http://localhost:{PORT}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Shutdown requested.")
