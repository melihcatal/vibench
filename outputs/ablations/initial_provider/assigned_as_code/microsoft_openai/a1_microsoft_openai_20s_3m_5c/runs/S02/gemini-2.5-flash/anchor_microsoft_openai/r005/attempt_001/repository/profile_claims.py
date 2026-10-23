import os
import jwt
import requests
from identity_models import UserProfileClaims, OAuthTokenResponse
from identity_client import IdentityClient, get_identity_client_config

def fetch_and_normalize_profile_claims(token_response: OAuthTokenResponse) -> UserProfileClaims:
    config = get_identity_client_config()
    client = IdentityClient(config['tenant_id'], config['client_id'], config['client_secret'])

    # If an ID token is available, decode it for claims
    if token_response.id_token:
        try:
            # MSAL (Azure AD) ID tokens are typically signed JWTs
            # For simplicity, we're just decoding without full signature verification here.
            # In a production app, you should verify the signature against the IdP's public keys.
            claims = jwt.decode(token_response.id_token, options={"verify_signature": False})
        except Exception as e:
            print(f"Error decoding ID token: {e}")
            claims = {}
    else:
        claims = {}

    # Optionally, fetch additional profile info from Microsoft Graph API using the access token
    if token_response.access_token:
        graph_url = "https://graph.microsoft.com/v1.0/me"
        headers = {'Authorization': f'Bearer {token_response.access_token}'}
        graph_response = requests.get(graph_url, headers=headers)
        if graph_response.ok:
            graph_data = graph_response.json()
            # Merge Graph API data, preferring it over ID token claims for common fields
            claims.update({
                'sub': graph_data.get('id', claims.get('sub')),
                'name': graph_data.get('displayName', claims.get('name')),
                'given_name': graph_data.get('givenName', claims.get('given_name')),
                'family_name': graph_data.get('surname', claims.get('family_name')),
                'email': graph_data.get('mail') or graph_data.get('userPrincipalName', claims.get('email')),
                # Add other relevant claims from Graph API
            })
        else:
            print(f"Error fetching from Microsoft Graph: {graph_response.status_code} - {graph_response.text}")

    # Normalize claims to our UserProfileClaims model
    normalized_claims = UserProfileClaims(
        sub=claims.get('sub', claims.get('oid', '')),  # 'oid' is object ID in Azure AD for user
        name=claims.get('name'),
        given_name=claims.get('given_name'),
        family_name=claims.get('family_name'),
        email=claims.get('email'),
        picture=claims.get('picture'),
        raw_claims=claims
    )

    return normalized_claims
