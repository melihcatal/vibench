import http.server
import urllib.parse
import urllib.request
import json

# PKCE flow data – replace with real values for production
CLIENT_ID = "YOUR_CLIENT_ID"
REDIRECT_URI = "http://localhost:8080/pkce_callback"
AUTHORIZATION_ENDPOINT = "https://login.salesforce.com/services/oauth2/authorize"
TOKEN_ENDPOINT = "https://login.salesforce.com/services/oauth2/token"


class PKCEHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        # Step 1: Generate code_verifier and code_challenge
        code_verifier = self._generate_pkce_verifier()
        code_challenge = self._generate_pkce_challenge(code_verifier)
        # Store verifier temporarily (here we keep it in memory; in real app use a db)
        self.server.pkce_verifier = code_verifier

        # Build authorization URL
        params = {
            "response_type": "code",
            "client_id": CLIENT_ID,
            "redirect_uri": REDIRECT_URI,
            "scope": "openid email profile",
            "code_challenge": code_challenge,
            "code_challenge_method": "S256",
        }
        query = urllib.parse.urlencode(params)
        auth_url = f"{AUTHORIZATION_ENDPOINT}?{query}"

        self.send_response(302)
        self.send_header("Location", auth_url)
        self.end_headers()

    def do_POST(self):
        # Step 2: Callback – exchange code for tokens
        if self.path != "/pkce_callback":
            self.send_response(404)
            self.end_headers()
            return
        content_length = int(self.headers.get("Content-Length", "0"))
        body = self.rfile.read(content_length)
        try:
            data = json.loads(body)
        except json.JSONDecodeError:
            self.send_response(400, "Bad Request")
            self.end_headers()
            return
        code = data.get("code")
        if not code or not self.server.pkce_verifier:
            self.send_response(400, "Invalid request")
            self.end_headers()
            return

        # Step 3: PKCE token exchange
        token_payload = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": REDIRECT_URI,
            "client_id": CLIENT_ID,
            "code_verifier": self.server.pkce_verifier,
        }
        token_response = self._post_token_request(token_payload)

        # Step 4: Return tokens to client (normally would store them server-side)
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(token_response).encode())

    @staticmethod
    def _generate_pkce_verifier(length: int = 128) -> str:
        import secrets, string
        alphabet = string.ascii_letters + string.digits + "-._~"
        return "".join(secrets.choice(alphabet) for _ in range(length))

    @staticmethod
    def _generate_pkce_challenge(verifier: str) -> str:
        import base64, hashlib
        hash_bytes = hashlib.sha256(verifier.encode()).digest()
        return base64.urlsafe_b64encode(hash_bytes).rstrip(b"=").decode()

    def _post_token_request(self, payload: dict):
        token_url = TOKEN_ENDPOINT
        body = urllib.parse.urlencode(payload).encode()
        req = urllib.request.Request(token_url, data=body, method="POST")
        with urllib.request.urlopen(req) as resp:
            token_body = resp.read().decode()
        return json.loads(token_body)

if __name__ == "__main__":
    # Simple server that keeps state in server.pkce_verifier
    server = http.server.HTTPServer(("0.0.0.0", 8080), PKCEHandler)
    print("PKCE login flow ready. Navigate to http://localhost:8080")
    server.serve_forever()
