import os
import secrets
import webbrowser
import http.server
import socketserver
from urllib.parse import urlparse, parse_qs

# Google Identity Platform OIDC example with PKCE
# Provider configuration: GOOGLE_CLIENT_ID, GOOGLE_REDIRECT_URI

CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
REDIRECT_URI = os.getenv('GOOGLE_REDIRECT_URI')

def generate_pkce_pair():
    code_verifier = secrets.token_urlsafe(32)
    code_challenge = secrets.token_urlsafe(43)  # base64url encode of SHA256 then strip padding
    # Simplified: create a base64url of SHA256 of code_verifier (no padding)
    import hashlib
    sha = hashlib.sha256(code_verifier.encode()).digest()
    code_challenge = base64.urlsafe_b64encode(sha).decode().rstrip('=')
    return code_verifier, code_challenge


def start_pkce_flow():
    code_verifier, code_challenge = generate_pkce_pair()
    auth_url = (
        "https://accounts.google.com/o/oauth2/v2/auth?"
        f"response_type=code&"
        f"client_id={CLIENT_ID}&"
        f"redirect_uri={REDIRECT_URI}&"
        "scope=openid%20email%20profile&"
        f"access_type=offline&"
        f"prompt=consent&"
        f"code_challenge={code_challenge}&"
        "code_challenge_method=S256"
    )
    print('Open this URL in your browser:')
    print(auth_url)
    webbrowser.open(auth_url)

    # Capture callback
    PORT = 8080
    handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(('', PORT), handler) as httpd:
        print(f"Listening on localhost:{PORT}")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            pass

if __name__ == '__main__':
    start_pkce_flow()
