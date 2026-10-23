import json
import os
from azure.identity import DefaultAzureCredential
from azure.cosmos import CosmosClient

def normalize_profile_claims(token_response):
    """Normalize OIDC ID token claims into a consistent internal model."""
    # The token response from MSAL contains an 'id_token' field
    id_token = token_response.get('id_token')
    if not id_token:
        raise ValueError('ID token not present in the token response')

    # Decode JWT payload (MSAL already parses it, but we re‑extract for clarity)
    # Using the 'python-jose' library; add as a dependency if not present
    from jose import jwt
    # Alternatively, use jwt.decode from PyJWT if available
    try:
        payload = jwt.decode(
            id_token,
            # In a real app you would fetch the signing keys from the provider's JWKS endpoint
            # For demo purposes we skip verification (NOT PRODUCTION!)
            verify=False,
        )
    except Exception as e:
        raise ValueError(f"Failed to decode JWT: {e}")

    # Extract common sub‑claims and map to our internal schema
    normalized = {
        "user_id": payload.get('sub'),
        "username": payload.get('name') or payload.get('preferred_username'),
        "email": payload.get('email'),
        "given_name": payload.get('given_name'),
        "family_name": payload.get('family_name'),
        "picture": payload.get('picture'),
        "locale": payload.get('locale'),
        "claims": payload,  # raw, for audit / debugging
    }
    return normalized

# Example usage – load a stored ID token from Cosmos DB and normalize it
if __name__ == "__main__":
    # Azure Cosmos DB settings (must be set in environment)
    COSMOS_URI = os.getenv('AZURE_COSMOS_URI')
    COSMOS_KEY = os.getenv('AZURE_COSMOS_KEY')
    DATABASE_NAME = os.getenv('AZURE_COSMOS_DATABASE')
    CONTAINER_NAME = os.getenv('AZURE_COSMOS_CONTAINER')

    if not all([COSMOS_URI, COSMOS_KEY, DATABASE_NAME, CONTAINER_NAME]):
        raise RuntimeError('Missing Cosmos DB configuration in environment variables')

    credential = DefaultAzureCredential()
    client = CosmosClient(COSMOS_URI, credential=credential)
    database = client.get_database_client(DATABASE_NAME)
    container = database.get_container_client(CONTAINER_NAME)

    # Suppose we stored the raw token JSON under the field 'id_token'
    item = container.read_item(item='example-id')  # replace with real item id
    raw_token = json.loads(item['id_token'])
    profile = normalize_profile_claims({'id_token': raw_token})
    print(json.dumps(profile, indent=2))
