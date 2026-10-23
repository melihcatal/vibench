import identity_client
import identity_models


def get_user_profile(access_token):
    client = identity_client.get_client()
    # Fetch federated user profile claims
    claims_raw = client.get_userinfo(access_token)
    # Normalize claims (e.g., map OIDC to internal schema)
    profile = identity_models.normalize_profile(claims_raw)
    return profile
