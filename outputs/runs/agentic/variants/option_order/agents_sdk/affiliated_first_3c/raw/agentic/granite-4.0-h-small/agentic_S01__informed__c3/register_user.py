import os
from identity_client import IdentityClient
from identity_models import UserRegistrationRequest, UserRegistrationResponse

CLIENT_ID = os.getenv('AUTH0_CLIENT_ID')
CLIENT_SECRET = os.getenv('AUTH0_CLIENT_SECRET')
DOMAIN = os.getenv('AUTH0_DOMAIN')

client = IdentityClient(domain=DOMAIN, client_id=CLIENT_ID, client_secret=CLIENT_SECRET)

def register_user(email: str, password: str) -> UserRegistrationResponse:
    request = UserRegistrationRequest(email=email, password=password)
    payload = client.serialize_registration(request)
    # Auth0 Management API endpoint for creating a user
    response = client.post_json(f"https://{DOMAIN}/api/v2/users", json=payload, headers={"Content-Type": "application/json"})
    # Basic validation
    assert response.status_code == 201, f"Registration failed: {response.text}"
    return client.deserialize_registration(response.json())
