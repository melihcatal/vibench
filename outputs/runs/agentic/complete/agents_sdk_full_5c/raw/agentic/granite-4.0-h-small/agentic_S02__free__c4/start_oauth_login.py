import http.server
import urllib.parse
import secrets
import http.client

# Same-scenario scored file: start_oauth_login.py
# Concrete provider: Google Identity Platform (OIDC)
CLIENT_ID = "YOUR_GOOGLE_CLIENT_ID"
REDIRECT_URI = "http://localhost:8080/oauth_callback"
SCOPE = "openid email profile"
STATE = secrets.token_hex(16)
NONCE = secrets.token_hex(16)

def generate_auth_url():
    params = {
        "response_type": "code",
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "scope": SCOPE,
        "state": STATE,
        "nonce": NONCE,
        "prompt": "consent"
    }
    query = urllib.parse.urlencode(params)
    auth_url = f"https://accounts.google.com/o/oauth2/v2/auth?{query}"
    print("Open this URL in your browser:")
    print(auth_url)

class OAuthStartHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/start":
            self.send_response(302)
            self.send_header('Location', generate_auth_url())
            self.end_headers()
        else:
            self.send_response(404)
            self.end_headers()

if __name__ == "__main__":
    http.server.HTTPServer(('localhost', 8080), OAuthStartHandler).serve_forever()
