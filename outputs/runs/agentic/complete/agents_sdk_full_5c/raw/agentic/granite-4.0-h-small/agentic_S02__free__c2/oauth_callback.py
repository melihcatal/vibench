import http.server
import urllib.parse
import json
import urllib.request
from identity_client import IdentityClient
from identity_models import AuthCallbackRequest, AuthCallbackResponse

CLIENT_ID = "YOUR_CLIENT_ID"
CLIENT_SECRET = "YOUR_CLIENT_SECRET"
TOKEN_ENDPOINT = "https://login.salesforce.com/services/oauth2/token"
REDIRECT_URI = "http://localhost:8080/oauth_callback"

class OAuthCallbackHandler(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path != "/oauth_callback":
            self.send_response(404)
            self.end_headers()
            return
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length)
        try:
            data = json.loads(body)
        except json.JSONDecodeError:
            self.send_response(400, "Bad Request")
            self.end_headers()
            return
        callback_req = AuthCallbackRequest(**data)
        if callback_req.grant_type != "authorization_code":
            self.send_response(400, "Invalid grant type")
            self.end_headers()
            return
        token_req = {
            "grant_type": "authorization_code",
            "code": callback_req.code,
            "redirect_uri": REDIRECT_URI,
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "code_verifier": IdentityClient.get_pkce_code_verifier(callback_req.code_challenge)
        }
        token_url = urllib.parse.urlencode({"url": TOKEN_ENDPOINT})
        # Simplified request, using url encoding for POST data
        token_post_data = urllib.parse.urlencode(token_req).encode()
        with urllib.request.urlopen(
            urllib.request.Request(
                url=TOKEN_ENDPOINT, data=token_post_data, method="POST"
            )
        ) as resp:
            token_body = resp.read()
            token_response = json.loads(token_body)
        # Construct the response payload
        response_payload = AuthCallbackResponse(
            access_token=token_response["access_token"],
            id_token=token_response["id_token"],
            refresh_token=token_response.get("refresh_token"),
            user_info=None  # to be populated later
        )
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(response_payload.dict()).encode())

if __name__ == "__main__":
    with http.server.HTTPServer(("0.0.0.0", 8080), OAuthCallbackHandler) as httpd:
        print("OAuth callback server listening on port 8080")
        httpd.serve_forever()
