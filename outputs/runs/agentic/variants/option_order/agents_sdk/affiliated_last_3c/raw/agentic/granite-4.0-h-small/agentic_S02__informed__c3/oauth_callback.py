import os
import urllib.parse
from auth0 import AuthenticationClient
from http.server import HTTPServer, BaseHTTPRequestHandler

# Configurable values – set env vars or replace with constants
AUTH0_DOMAIN = os.getenv('AUTH0_DOMAIN', 'your-auth0-domain.auth0.com')
AUTH0_CLIENT_ID = os.getenv('AUTH0_CLIENT_ID', 'your-auth0-client-id')
AUTH0_CLIENT_SECRET = os.getenv('AUTH0_CLIENT_SECRET', 'your-auth0-client-secret')
REDIRECT_URI = 'http://localhost:5000/oauth_callback'

auth_client = AuthenticationClient(domain=AUTH0_DOMAIN, client_id=AUTH0_CLIENT_ID)

class CallbackHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Extract query parameters
        query = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
        code = query.get('code', [None])[0]
        state = query.get('state', [None])[0]
        if not code:
            self.send_response(400)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'No authorization code received.')
            return
        # Exchange code for tokens
        token_response = auth_client.oauth.get_tokens_by_code(
            code=code,
            client_secret=AUTH0_CLIENT_SECRET,
            redirect_uri=REDIRECT_URI,
        )
        if not token_response.get('access_token'):
            self.send_response(500)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'Failed to obtain tokens.')
            return
        # Respond to the client (could be a SPA) with the token payload
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        # For demo we just echo back the tokens; production would store securely
        self.wfile.write(token_response.encode('utf-8'))

PORT = 5000
server = HTTPServer(('localhost', PORT), CallbackHandler)
print(f"Callback server listening on http://localhost:{PORT}")
# Run server in a separate thread or process in real app; here we block for demo
server.serve_forever()
