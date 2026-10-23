import requests
import jwt
from jwt.algorithms import RSAAlgorithm


def fetch_and_normalize_profile_claims(access_token, id_token):
    userinfo_endpoint = "https://openidconnect.googleapis.com/v1/userinfo"

    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(userinfo_endpoint, headers=headers)
    userinfo = response.json()

    jwks_url = "https://www.googleapis.com/oauth2/v3/certs"
    jwks_client = jwt.PyJWKClient(jwks_url)

    try:
        signing_key = jwks_client.get_signing_key_from_jwt(id_token)
        decoded_id_token = jwt.decode(
            id_token,
            signing_key.key,
            algorithms=["RS256"],
            audience=os.environ.get("GOOGLE_OAUTH_CLIENT_ID"),
        )
    except Exception as e:
        decoded_id_token = {}

    normalized_claims = {
        "sub": userinfo.get("sub") or decoded_id_token.get("sub"),
        "email": userinfo.get("email") or decoded_id_token.get("email"),
        "email_verified": userinfo.get("email_verified")
        or decoded_id_token.get("email_verified", False),
        "name": userinfo.get("name") or decoded_id_token.get("name"),
        "given_name": userinfo.get("given_name") or decoded_id_token.get("given_name"),
        "family_name": userinfo.get("family_name")
        or decoded_id_token.get("family_name"),
        "picture": userinfo.get("picture") or decoded_id_token.get("picture"),
        "locale": userinfo.get("locale") or decoded_id_token.get("locale"),
        "provider": "google",
    }

    return normalized_claims
