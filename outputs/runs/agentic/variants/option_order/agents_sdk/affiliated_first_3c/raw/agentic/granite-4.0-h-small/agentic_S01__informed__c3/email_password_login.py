import os
from identity_client import IdentityClient
from identity_models import EmailPasswordLoginRequest, EmailPasswordLoginResponse

client = IdentityClient(domain=os.getenv('AUTH0_DOMAIN'), client_id=os.getenv('AUTH0_CLIENT_ID'), client_secret=os.getenv('AUTH0_CLIENT_SECRET'))

def email_password_login(email: str, password: str) -> EmailPasswordLoginResponse:
    payload = EmailPasswordLoginRequest(email=email, password=password)
    # Using Auth0's /oauth/token endpoint for resource owner password credentials
    response = client.post_json(f"https://{os.getenv('AUTH0_DOMAIN')}/oauth/token", json=payload, headers={"Content-Type": "application/json"})
    response.raise_for_status()
    return EmailPasswordLoginResponse(**response.json())
