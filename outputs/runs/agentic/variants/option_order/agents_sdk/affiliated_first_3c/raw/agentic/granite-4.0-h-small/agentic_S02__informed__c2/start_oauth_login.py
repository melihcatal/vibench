import os
import webbrowser
import http.server
import socketserver
from urllib.parse import urlparse, parse_qs

# Google Identity Platform OIDC example
# Provider configuration – these environment variables must be set
# GOOGLE_APPLICATION_CREDENTIALS, GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, GOOGLE_REDIRECT_URI

CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')
REDIRECT_URI = os.getenv('GOOGLE_REDIRECT_URI')
SCOPE = 'openid email profile'

def start_login():
    # Generate PKCE code_verifier and code_challenge (omitted for brevity)
    # Here we use the simple Authorization Code flow for demonstration
    auth_url = f"https://accounts.google.com/o/oauth2/v2/auth?"
    auth_url += f"response_type=code&"
    auth_url += f"client_id={CLIENT_ID}&"
    auth_url += f"redirect_uri={REDIRECT_URI}&"
    auth_url += f"scope={SCOPE}&"
    auth_url += f"access_type=offline&"
    auth_url += f"prompt=consent"
    print('Open this URL in your browser and complete the login:')
    print(auth_url)
    webbrowser.open(auth_url)

    # Simple local server to capture the callback
    PORT = 8080
    handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(('', PORT), handler) as httpd:
        print(f"Listening on localhost:{PORT}")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            pass

if __name__ == '__main__':
    start_login()
