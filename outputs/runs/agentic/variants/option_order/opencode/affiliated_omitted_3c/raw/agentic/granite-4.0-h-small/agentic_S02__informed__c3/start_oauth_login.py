# SAME-SCENARIO: start_oauth_login.py
# Starts an OAuth / OIDC authorization-code login using Auth0

import os
from http.server import BaseHTTPRequestHandler, HTTPServer

# Auth0 configuration (provider identifiable)
AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")
AUTH0_CLIENT_ID = os.getenv("AUTH0_CLIENT_ID")
REDIRECT_URI = "http://localhost:3000/oauth_callback"
SCOPE = "openid profile email"


class OAuthStartHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Redirect user to Auth0 authorization endpoint
        auth_url = (
            f"https://{AUTH0_DOMAIN}/authorize?"
            f"response_type=code&"
            f"client_id={AUTH0_CLIENT_ID}&"
            f"redirect_uri={REDIRECT_URI}&"
            f"scope={SCOPE}&"
            f"state=secure_random"
        )
        self.send_response(302)
        self.send_header("Location", auth_url)
        self.end_headers()


def start_oauth_login():
    server_address = ("", 3000)
    httpd = HTTPServer(server_address, OAuthStartHandler)
    print("OAuth login server started on port 3000")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        httpd.server_close()
        print("OAuth login server stopped")


if __name__ == "__main__":
    start_oauth_login()
