import jwt
from identity_models import NormalizedUser

def get_normalized_profile(id_token: str) -> NormalizedUser:
    """
    Decodes the ID token from Microsoft Entra and normalizes the claims.
    
    NOTE: In a production scenario, you must validate the token signature.
    This example decodes without validation for simplicity.
    """
    # In a real app, you would fetch keys from the JWKS URI and validate the signature.
    # jwks_uri = "https://login.microsoftonline.com/{tenant_id}/discovery/v2.0/keys"
    unverified_claims = jwt.decode(id_token, options={"verify_signature": False})

    # Normalize claims
    user = NormalizedUser(
        user_id=unverified_claims.get("oid"), # Object ID is the immutable user identifier
        email=unverified_claims.get("email") or unverified_claims.get("preferred_username"),
        name=unverified_claims.get("name"),
        username=unverified_claims.get("preferred_username"),
        given_name=unverified_claims.get("given_name"),
        family_name=unverified_claims.get("family_name"),
    )
    
    return user
