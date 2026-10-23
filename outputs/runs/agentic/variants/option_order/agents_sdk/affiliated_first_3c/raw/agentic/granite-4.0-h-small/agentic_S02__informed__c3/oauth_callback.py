import os
import json
from identity_client import IdentityClient
from identity_models import AuthResponse

def oauth_callback(request):
    """
    Handler for the OAuth callback endpoint.
    Expects 'code' and 'state' query parameters.
    """
    client = IdentityClient()
    AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")
    AUTH0_CLIENT_ID = os.getenv("AUTH0_CLIENT_ID")
    AUTH0_CLIENT_SECRET = os.getenv("AUTH0_CLIENT_SECRET")

    # Retrieve parameters from the request (e.g., Flask, FastAPI, etc.)
    code = request.args.get("code")
    state = request.args.get("state")
    if not code or not state:
        return json_response({"error": "Missing code or state"}, 400)

    # Exchange authorization code for tokens
    token_endpoint = f"https://{AUTH0_DOMAIN}/oauth/token"
    data = {
        "grant_type": "authorization_code",
        "code": code,
        "client_id": AUTH0_CLIENT_ID,
        "client_secret": AUTH0_CLIENT_SECRET,
        "redirect_uri": request.base_url.rstrip('/')
    }
    response = requests.post(token_endpoint, data=data)
    response.raise_for_status()
    token_data = response.json()

    # Construct a simple AuthResponse model
    auth_resp = AuthResponse(
        access_token=token_data.get("access_token"),
        id_token=token_data.get("id_token"),
        refresh_token=token_data.get("refresh_token"),
        expires_in=token_data.get("expires_in")
    )
    return json_response(auth_resp.dict(), 200)

def json_response(payload, status=200):
    return {
        "status_code": status,
        "body": json.dumps(payload)
    }

if __name__ == "__main__":
    # Dummy test using Flask-like request simulation
    class DummyRequest:
        def __init__(self, args):
            self.args = args
            self.base_url = "https://example.com/callback"
    test_req = DummyRequest({"code": "test-code", "state": "test-state"})
    print(oauth_callback(test_req))
