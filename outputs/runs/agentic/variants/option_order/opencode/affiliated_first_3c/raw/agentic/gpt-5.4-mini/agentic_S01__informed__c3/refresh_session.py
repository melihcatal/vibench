from identity_client import auth0_api, oauth_token_payload, post_json
from identity_models import token_bundle


def refresh_session(refresh_token: str):
    payload = oauth_token_payload("refresh_token", refresh_token=refresh_token)
    data = post_json(auth0_api("/oauth/token"), payload)
    return token_bundle(
        data.get("access_token", ""),
        data.get("refresh_token", refresh_token),
        data.get("id_token", ""),
    )
