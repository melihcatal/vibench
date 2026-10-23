import msal
from identity_client import get_microsoft_entra_config
from identity_models import TokenResponse, UserProfile


def fetch_profile_claims(tokens: TokenResponse) -> UserProfile:
    config = get_microsoft_entra_config(public_client=True)
    app = msal.ConfidentialClientApplication(
        config["client_id"], authority=config["authority"]
    )
    claims = app.decode_id_token(tokens.id_token)
    return UserProfile(
        sub=claims["sub"],
        email=claims.get("email"),
        name=claims.get("name"),
        given_name=claims.get("given_name"),
        family_name=claims.get("family_name"),
        preferred_username=claims.get("preferred_username"),
    )
