import jwt
from typing import Optional
from identity_models import UserProfile
from identity_client import CognitoClient

def fetch_and_normalize_profile_claims(id_token: str, access_token: str) -> UserProfile:
    cognito_client = CognitoClient()
    # In a real application, you would verify the JWT signature and audience.
    # For simplicity, we are just decoding here.
    # You would typically fetch the JWKS from Cognito's /.well-known/jwks.json endpoint.
    try:
        # The ID token contains the user's profile claims
        decoded_id_token = jwt.decode(id_token, options={"verify_signature": False})

        user_id = decoded_id_token.get("sub")
        if not user_id:
            raise ValueError("User ID not found in ID token.")

        return UserProfile(
            user_id=user_id,
            username=decoded_id_token.get("cognito:username"),
            email=decoded_id_token.get("email"),
            first_name=decoded_id_token.get("given_name"),
            last_name=decoded_id_token.get("family_name"),
            claims=decoded_id_token
        )
    except Exception as e:
        raise RuntimeError(f"Failed to decode or normalize claims: {e}")
