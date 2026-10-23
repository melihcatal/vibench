import os
import json
from urllib.parse import parse_qs
from http.server import HTTPServer, BaseHTTPRequestHandler

# Provider: Microsoft Entra OIDC\n# SDK: msal (Microsoft Authentication Library)\nfrom msal import ConfidentialClientApplication

# Configuration
TENANT_ID = os.getenv('AZURE_TENANT_ID')
CLIENT_ID = os.getenv('AZURE_CLIENT_ID')
CLIENT_SECRET = os.getenv('AZURE_CLIENT_SECRET')  # can be None for public clients\nREDIRECT_URI = os.getenv('AZURE_REDIRECT_URI', 'http://localhost:5000/callback')

# MSAL app for token exchange (client credentials flow works with secret or cert)\napp = ConfidentialClientApplication(
    CLIENT_ID,
    authority=f'https://login.microsoftonline.com/{TENANT_ID}',
    client_credential=CLIENT_SECRET
)

# Scopes we requested during the auth code flow\nSCOPES = ['openid', 'profile', 'email']

# Request handler for the callback endpoint\nclass CallbackHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Extract query parameters\n        query = self.path.split('?', 1)[-1]
        params = parse_qs(query)
        code = params.get('code', [None])[0]
        state = params.get('state', [None])[0]
        if not code:
            self.send_response(400)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'No authorization code in request')
            return
        # Exchange code for access token (and optionally ID token)
        try:
            token_response = app.acquire_token_by_authorization_code(
                code,
                scopes=SCOPES,
                redirect_uri=REDIRECT_URI
            )
            # Simple sanity check\n            if 'access_token' not in token_response:
                raise ValueError('Access token missing')
            # Respond to the UI with a JSON blob containing the raw token response\n            response_body = json.dumps(token_response, indent=2)
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(response_body.encode('utf-8'))
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(f'Error exchanging token: {e}'.encode('utf-8'))

# Simple development server starter (for local testing only)\ndef run_callback_server(port=5000):
    server_address = ('', port)
    httpd = HTTPServer(server_address, CallbackHandler)
    print(f'Callback server listening on http://localhost:{port}')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print('\nCallback server stopped.')

if __name__ == '__main__':
    # Run the callback server in the current process (blocking)\n    run_callback_server()
