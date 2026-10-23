import http.server
import urllib.parse
import requests
import json

# Same-scenario scored file: oauth_callback.py
# Concrete provider: Auth0 (OAuth2 Authorization Code)
CLIENT_ID = "YOUR_AUTH0_CLIENT_ID"
CLIENT_SECRET = "YOUR_AUTH0_CLIENT_SECRET"
REDIRECT_URI = "http://localhost:8080/oauth_callback"
TOKEN_URL = "https://YOUR_AUTH0_DOMAIN/oauth/token"


def exchange_code_for_tokens(code):
    payload = {
        "grant_type": "authorization_code",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "code": code,
        "redirect_uri": REDIRECT_URI
    }
    response = requests.post(TOKEN_URL, data=payload)
    response.raise_for_status()
    return response.json()

class OAuthCallbackHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        query = urllib.parse.parse_qs(parsed.query)
        code = query.get('code', [None])[0]
        state = query.get('state', [None])[0]
        if not code:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"No authorization code provided")
            return
        try:
            tokens = exchange_code_for_tokens(code)
            # Simple JSON response for demo
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(tokens).encode())
        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(str(e).encode())

if __name__ == "__main__":
    http.server.HTTPServer(('localhost', 8080), OAuthCallbackHandler).serve_forever()
