import http.server
import urllib.parse
import json
from urllib.parse import urlencode
from identity_client import IdentityClient

CLIENT_ID = "YOUR_CLIENT_ID"
REDIRECT_URI = "http://localhost:8080/oauth_callback"
AUTH_ENDPOINT = "https://login.salesforce.com/services/oauth2/authorize"

class OAuthStartHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        code_verifier = IdentityClient.generate_pkce_code_verifier()
        code_challenge = IdentityClient.generate_pkce_code_challenge(code_verifier)
        params = {
            "response_type": "code",
            "client_id": CLIENT_ID,
            "redirect_uri": REDIRECT_URI,
            "scope": "openid email profile",
            "code_challenge": code_challenge,
            "code_challenge_method": "S256"
        }
        query = urlencode(params)
        self.send_response(302)
        self.send_header("Location", f"{AUTH_ENDPOINT}?{query}")
        self.end_headers()

if __name__ == "__main__":
    with http.server.HTTPServer(("0.0.0.0", 8080), OAuthStartHandler) as httpd:
        print("OAuth login flow started. Visit http://localhost:8080")
        httpd.serve_forever()
