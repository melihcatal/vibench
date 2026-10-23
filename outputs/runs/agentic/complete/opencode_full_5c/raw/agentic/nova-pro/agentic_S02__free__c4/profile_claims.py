from identity_client import auth0_client
from identity_models import ProfileClaims


def profile_claims(access_token: str):
    userinfo = auth0_client.userinfo(access_token)
    claims = ProfileClaims(
        sub=userinfo.get("sub", ""),
        name=userinfo.get("name", ""),
        email=userinfo.get("email", ""),
    )
    print(f"Profile Claims: {claims}")
    return claims
