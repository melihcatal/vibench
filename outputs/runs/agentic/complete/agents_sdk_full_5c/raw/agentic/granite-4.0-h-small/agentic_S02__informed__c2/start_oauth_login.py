import os
import webbrowser
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

# Provider: Microsoft Entra OIDC\n# SDK: msal (Microsoft Authentication Library)\nfrom msal import ConfidentialClientApplication

# Configuration (environment variables or config file)\nTENANT_ID = os.getenv('AZURE_TENANT_ID')\nCLIENT_ID = os.getenv('AZURE_CLIENT_ID')\nREDIRECT_URI = os.getenv('AZURE_REDIRECT_URI', 'http://localhost:5000/callback')

# Create the MSAL app instance\napp = ConfidentialClientApplication(\n    CLIENT_ID,\n    authority=f'https://login.microsoftonline.com/{TENANT_ID}',\n    client_credential=None  # for public client; could also use client secret or cert\n)

# Define scopes needed for the federated user profile\nSCOPES = ['openid', 'profile', 'email']

# Global to capture the callback result\ncallback_result = {'code': None, 'state': None}\n
class OAuthCallbackHandler(BaseHTTPRequestHandler):\n    def do_GET(self):\n        query = urlparse(self.path).query\n        params = parse_qs(query)\n        self.send_response(200)\n        self.send_header('Content-type', 'text/html')\n        self.end_headers()\n        # Store the code and state\n        callback_result['code'] = params.get('code', [None])[0]\n        callback_result['state'] = params.get('state', [None])[0]\n        self.wfile.write(b"<html><body><script>window.close();</script>Authentication callback received.</body></html>")\n
# Helper to start a simple HTTP server in a thread to listen for the callback\ndef start_callback_server():\n    server_address = ('', 5000)\n    httpd = HTTPServer(server_address, OAuthCallbackHandler)\n    httpd.timeout = 5  # short timeout for fast handling\n    return httpd\n
# Function to initiate the OAuth2 authorization-code flow\ndef start_oauth_login():\n    # Build the authorization URL\n    auth_url = app.authority + '/oauth2/v2.0/authorize?' + app.get_authorization_request_url(\n        SCOPES,\n        redirect_uri=REDIRECT_URI,\n        state='post_login'  # CSRF protection token\n    )\n    print('Open the following URL in your browser and complete login:\n', auth_url)\n    # Start the callback server in a background thread\n    server = start_callback_server()\n    server_thread = threading.Thread(target=server.serve_forever)\n    server_thread.daemon = True\n    server_thread.start()\n    # Open the browser\n    webbrowser.open(auth_url)\n    # Wait until we capture the code\n    while callback_result['code'] is None:\n        threading.Event().wait(0.5)\n    # Shut down the server\n    server.shutdown()\n    server.server_close()\n    print('Received authorization code. Next steps would be to exchange it for tokens.')\n
if __name__ == '__main__':\n    start_oauth_login()\n