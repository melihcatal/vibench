import os
from typing import TypedDict
from identity_models import ProviderUserClaim
from identity_client import IdentityClient

# Google Identity Platform OIDC example
GOOGLE_IDP_USERINFO_ENDPOINT = "https://openidconnect.googleapis.com/v1/userinfo"
GOOGLE_IDP_ISSUER = "https://accounts.google.com"


class UserProfile(TypedDict):
    sub: str
    email: str
    email_verified: bool
    name: str
    picture: str
    locale: str


def profile_claims(token_response: Auth0TokenResponse) -> ProviderUserClaim:
    """Fetch and normalize federated user profile claims from Google's userinfo endpoint.
    Returns a ProviderUserClaim structure with normalized fields.
    """
    id_token = token_response.id_token
    userinfo = IdentityClient.get_userinfo(id_token)
    normalized = {
        "sub": userinfo.get("sub"),
        "email": userinfo.get("email"),
        "email_verified": userinfo.get("email_verified"),
        "name": userinfo.get("name"),
        "picture": userinfo.get("picture"),
        "locale": userinfo.get("locale"),
    }
    return ProviderUserClaim(**normalized)
