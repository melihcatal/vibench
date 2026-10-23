from identity_client import IdentityClient
from identity_models import PasswordResetRequest
import os

def start_password_reset(email: str) -> bool:
    client = IdentityClient(domain=os.getenv('AUTH0_DOMAIN'), client_id=os.getenv('AUTH0_CLIENT_ID'), client_secret=os.getenv('AUTH0_CLIENT_SECRET'))
    payload = PasswordResetRequest(client_id=os.getenv('AUTH0_CLIENT_ID'), email=email)
    # Using Auth0 password reset ticket endpoint
    response = client.post_json(f'https://{os.getenv('AUTH0_DOMAIN')}/api/v2/tickets/password-reset', json=payload, headers={'Content-Type': 'application/json'})
    response.raise_for_status()
    return response.status_code == 201