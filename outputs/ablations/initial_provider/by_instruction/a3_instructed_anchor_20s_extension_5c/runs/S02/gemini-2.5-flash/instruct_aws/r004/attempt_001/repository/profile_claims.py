import json
import jwt

def fetch_and_normalize_claims(id_token: str):
    """
    Decodes the ID token and normalizes the claims.
    In a real application, you might also fetch claims from the UserInfo endpoint.
    """
    try:
        # For simplicity, we are not verifying the token signature here.
        # In a production environment, you MUST verify the token signature and expiration.
        # You would typically get the public keys from Cognito's JWKS endpoint.
        decoded_token = jwt.decode(id_token, options={"verify_signature": False})

        # Normalize claims (example normalization)
        normalized_claims = {
            "sub": decoded_token.get("sub"),
            "email": decoded_token.get("email"),
            "email_verified": decoded_token.get("email_verified", False),
            "name": decoded_token.get("name", f"{decoded_token.get('given_name', '')} {decoded_token.get('family_name', '')}".strip()),
            "given_name": decoded_token.get("given_name"),
            "family_name": decoded_token.get("family_name"),
            "preferred_username": decoded_token.get("preferred_username"),
            "cognito:username": decoded_token.get("cognito:username"),
        }
        return normalized_claims
    except jwt.exceptions.DecodeError as e:
        print(f"Error decoding ID token: {e}")
        raise
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        raise

if __name__ == "__main__":
    # Example usage: Replace with a valid ID token from a Cognito login
    example_id_token = "eyJraWQiOiJ..."
    try:
        claims = fetch_and_normalize_claims(example_id_token)
        print("Normalized User Claims:")
        print(json.dumps(claims, indent=2))
    except Exception as e:
        print(f"Error: {e}")
