import os
import webbrowser
import base64
import hashlib
import json
import http.server
import socketserver
import requests
from urllib.parse import urlencode, urlparse, parse_qs

# Auth0 Configuration - Replace with your Auth0 domain and client ID
AUTH0_DOMAIN = os.environ.get("AUTH0_DOMAIN", "YOUR_AUTH0_DOMAIN.auth0.com")
AUTH0_CLIENT_ID = os.environ.get("AUTH0_CLIENT_ID", "YOUR_AUTH0_CLIENT_ID")
AUTH0_CALLBACK_PORT = os.environ.get("AUTH0_CALLBACK_PORT", 8080)
AUTH0_CALLBACK_URL = f"http://localhost:{AUTH0_CALLBACK_PORT}/callback"

# PKCE helper functions
def generate_random_string(length=32):
    return base64.urlsafe_b64encode(os.urandom(length)).rstrip(b'=').decode('utf-8')

def sha256_base64url_encode(data):
    hashed = hashlib.sha256(data.encode('utf-8')).digest()
    return base64.urlsafe_b64encode(hashed).rstrip(b'=').decode('utf-8')

def pkce_challenge_pair():
    code_verifier = generate_random_string(64)
    code_challenge = sha256_base64url_encode(code_verifier)
    return code_verifier, code_challenge

# HTTP server to handle the callback
class Auth0CallbackHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith("/callback"):
            query_params = parse_qs(urlparse(self.path).query)
            code = query_params.get("code", [None])[0]
            error = query_params.get("error", [None])[0]

            if error:
                self.send_response(200)
                self.end_headers()
                self.wfile.write(f"<html><body><h1>Error: {error}</h1><p>{query_params.get('error_description', [''])[0]}</p></body></html>".encode('utf-8'))
                print(f"Auth0 Error: {error} - {query_params.get('error_description', [''])[0]}")
                self.server.auth_code = None
            elif code:
                self.send_response(200)
                self.end_headers()
                self.wfile.write(b"<html><body><h1>Successfully received authorization code. You can close this window.</h1></body></html>")
                self.server.auth_code = code
            else:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b"<html><body><h1>Bad Request: No authorization code received.</h1></body></html>")
            
            # Stop the server after handling the callback
            self.server.shutdown()
        else:
            super().do_GET()

def get_authorization_code(code_challenge, state):
    authorize_url = f"https://{AUTH0_DOMAIN}/authorize"
    params = {
        "audience": f"https://{AUTH0_DOMAIN}/api/v2/",  # Or your specific API audience
        "scope": "openid profile email",
        "response_type": "code",
        "client_id": AUTH0_CLIENT_ID,
        "code_challenge": code_challenge,
        "code_challenge_method": "S256",
        "redirect_uri": AUTH0_CALLBACK_URL,
        "state": state,
    }
    webbrowser.open(f"{authorize_url}?{urlencode(params)}")

    with socketserver.TCPServer(("localhost", int(AUTH0_CALLBACK_PORT)), Auth0CallbackHandler) as httpd:
        httpd.auth_code = None
        print(f"Waiting for Auth0 callback on {AUTH0_CALLBACK_URL}...")
        httpd.serve_forever()
        return httpd.auth_code

def exchange_code_for_token(code, code_verifier):
    token_url = f"https://{AUTH0_DOMAIN}/oauth/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "grant_type": "authorization_code",
        "client_id": AUTH0_CLIENT_ID,
        "code_verifier": code_verifier,
        "code": code,
        "redirect_uri": AUTH0_CALLBACK_URL,
    }
    response = requests.post(token_url, headers=headers, data=data)
    response.raise_for_status()
    return response.json()

def main():
    print("Starting PKCE Login Flow...")

    code_verifier, code_challenge = pkce_challenge_pair()
    state = generate_random_string()

    print(f"Generated Code Verifier: {code_verifier}")
    print(f"Generated Code Challenge: {code_challenge}")
    print(f"Generated State: {state}")

    auth_code = get_authorization_code(code_challenge, state)

    if auth_code:
        print(f"Received Authorization Code: {auth_code}")
        print("Exchanging authorization code for tokens...")
        try:
            tokens = exchange_code_for_token(auth_code, code_verifier)
            print("Successfully obtained tokens:")
            print(json.dumps(tokens, indent=2))

            # You can now use tokens["access_token"] to make API calls
            # and tokens["id_token"] for user information
        except requests.exceptions.RequestException as e:
            print(f"Error exchanging code for tokens: {e}")
            if e.response:
                print(e.response.json())
    else:
        print("Failed to get authorization code.")

if __name__ == "__main__":
    main()
