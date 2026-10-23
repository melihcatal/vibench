import http.server
import urllib.parse
import secrets
import requests
import json

# Same-scenario scored file: pkce_login.py
# Concrete provider: Google Identity Platform (PKCE)
CLIENT_ID = "YOUR_GOOGLE_CLIENT_ID"
REDIRECT_URI = "http://localhost:8080/oauth_callback"


def generate_code_verifier():
    return secrets.token_urlsafe(32)


def generate_code_challenge(verifier):
    import hashlib
    return hashlib.sha256(verifier.encode()).hexdigest()


def build_pkce_auth_url():
    verifier = generate_code_verifier()
    challenge = generate_code_challenge(verifier)
    params = {
        "response_type": "code",
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "scope": "openid email profile",
        "code_challenge": challenge,
        "code_challenge_method": "S256",
        "state": secrets.token_hex(16),
        "nonce": secrets.token_hex(16)
    }
    query = urllib.parse.urlencode(params)
    auth_url = f"https://accounts.google.com/o/oauth2/v2/auth?{query}"
    print("Open this URL in your browser:", auth_url)
    return auth_url, verifier

class PKCEStartHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/pkce_start":
            auth_url, verifier = build_pkce_auth_url()
            # Store verifier in memory for demo (not production)
            self.send_response(302)
            self.send_header('Location', auth_url)
            self.end_headers()
        else:
            self.send_response(404)
            self.end_headers()

if __name__ == "__main__":
    http.server.HTTPServer(('localhost', 8080), PKCEStartHandler).serve_forever()
