
import base64
import hashlib
import os
import webbrowser
import requests
import http.server
import socketserver
import urllib.parse
import threading

# Configuration for Google OAuth 2.0
CLIENT_ID = "YOUR_GOOGLE_CLIENT_ID"  # Replace with your actual Google Client ID
REDIRECT_URI = "http://localhost:8080/callback"
AUTH_ENDPOINT = "https://accounts.google.com/o/oauth2/v2/auth"
TOKEN_ENDPOINT = "https://oauth2.googleapis.com/token"

def generate_pkce_pair():
    verifier = base64.urlsafe_b64encode(os.urandom(32)).rstrip(b'=').decode('utf-8')
    challenge = base64.urlsafe_b64encode(
        hashlib.sha256(verifier.encode('utf-8')).digest()
    ).rstrip(b'=').decode('utf-8')
    return verifier, challenge

class OAuth2CallbackHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(b"<html><body><h1>Authentication successful!</h1><p>You can close this window.</p></body></html>")

        query_params = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
        global auth_code
        if 'code' in query_params:
            auth_code = query_params['code'][0]
        else:
            auth_code = None
        
        # Shut down the server after receiving the code
        # This is a bit hacky for a simple example, in a real app you'd likely have a more robust way
        threading.Thread(target=self.server.shutdown).start()

def main():
    global auth_code
    auth_code = None

    code_verifier, code_challenge = generate_pkce_pair()

    params = {
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "response_type": "code",
        "scope": "openid email profile", # Example scopes
        "code_challenge": code_challenge,
        "code_challenge_method": "S256",
        "access_type": "offline", # To get a refresh token
        "prompt": "consent" # To ensure refresh token is always returned
    }

    auth_url = f"{AUTH_ENDPOINT}?{urllib.parse.urlencode(params)}"
    print(f"Please open this URL in your browser to authorize: {auth_url}")
    webbrowser.open(auth_url)

    # Start a simple HTTP server to catch the redirect
    PORT = 8080
    Handler = OAuth2CallbackHandler
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"Waiting for authorization code on port {PORT}...")
        httpd.serve_forever() # This will block until the server is shut down

    if auth_code:
        print(f"Received authorization code: {auth_code}")

        token_params = {
            "client_id": CLIENT_ID,
            "redirect_uri": REDIRECT_URI,
            "code_verifier": code_verifier,
            "code": auth_code,
            "grant_type": "authorization_code",
        }

        try:
            response = requests.post(TOKEN_ENDPOINT, data=token_params)
            response.raise_for_status() # Raise HTTPError for bad responses (4xx or 5xx)
            token_data = response.json()
            
            print("\nToken Exchange Successful:")
            print(f"Access Token: {token_data.get('access_token')}")
            print(f"ID Token: {token_data.get('id_token')}")
            print(f"Refresh Token: {token_data.get('refresh_token')}")
            print(f"Expires In: {token_data.get('expires_in')} seconds")
            print(f"Scope: {token_data.get('scope')}")

        except requests.exceptions.RequestException as e:
            print(f"Error during token exchange: {e}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"Response content: {e.response.text}")
    else:
        print("Authorization code not received.")

if __name__ == "__main__":
    main()
