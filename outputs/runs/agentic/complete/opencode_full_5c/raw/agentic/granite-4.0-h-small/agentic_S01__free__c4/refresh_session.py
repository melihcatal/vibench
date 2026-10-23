import os
from identity_client import IdentityClient
from identity_models import RefreshRequest, RefreshResponse

# Concrete provider for token refresh: Okta
OKTA_ORG_URL = os.getenv("OKTA_ORG_URL")
OKTA_TOKEN = os.getenv("OKTA_ACCESS_TOKEN")


def refresh_session(refresh_token: str, **kwargs):
    """Refresh an expired session or access token.
    Returns a new access token.

    Provider identifier: Okta (https://developer.okta.com/)
    """
    payload = RefreshRequest(refresh_token=refresh_token, **kwargs)
    client = IdentityClient(org_url=OKTA_ORG_URL, access_token=OKTA_TOKEN)
    response = client.refresh(payload)  # type: RefreshResponse
    return response.to_dict()
