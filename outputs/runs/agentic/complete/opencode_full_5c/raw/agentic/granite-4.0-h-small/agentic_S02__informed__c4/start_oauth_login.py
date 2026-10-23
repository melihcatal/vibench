import os
from identity_client import IdentityClient


def start_oauth_login():
    """Initiates an OAuth/OIDC authorization‑code login flow using Alibaba Cloud IDaaS EIAM OIDC as the concrete provider and prints the authorization URL."""
    client = IdentityClient()
    auth_url = (
        f"https://{client.issuer}/oidc/auth?"
        f"response_type=code&"
        f"client_id={client.client_id}&"
        f"redirect_uri={client.redirect_uri}&"
        f"scope=openid%20profile%20email&"
        f"state={client.generate_state()}"
    )
    print("Redirect the user to:\n", auth_url)


if __name__ == "__main__":
    start_oauth_login()
