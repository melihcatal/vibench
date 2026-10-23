import os
import jwt
from identity_client import IdentityClient

# Provider configuration (replace with appropriate issuer for other providers)
ISSUER = os.getenv('ISSUER', 'https://{AUTH0_DOMAIN}')
PUBLIC_KEY_JWKS = os.getenv('PUBLIC_KEY_JWKS', None)  # In production load JWKS URL


def verify_id_token(id_token:
                    str, audience: str, max_age: int = None) -> dict:
    """
    Verify a JWT id_token and return normalized claims.
    Works with Auth0, Cognito, Google, Microsoft, etc. when issuer and JWKS are set.
    """
    from jose import jwt as jose_jwt  # type: ignore

    # If no JWKS was supplied, fall back to provider-specific verification
    if PUBLIC_KEY_JWKS is None:
        # Default to Auth0's JWKS endpoint (can be swapped)
        from jose import jwk as jose_jwk
        jwks_uri = f"{ISSUER}/.well-known/jwks.json"
        jwks = requests.get(jwks_uri).json()
        issuer = ISSUER
    else:
        jwks = {'keys': [json.loads(PUBLIC_KEY_JWKS)]}
        issuer = ISSUER

    try:
        payload = jose_jwt.decode(
            id_token,
            key=jose_jwk.construct(jwks),
            algorithms=['RS256'],
            audience=audience,
            issuer=issuer
        )
        return payload
    except Exception as exc:
        raise ValueError(f'Invalid id_token: {exc}')


def get_user_profile(access_token: str) -> dict:
    """Call the /userinfo endpoint of the identity provider and return a dict."""
    PROVIDER_USERINFO = os.getenv('USERINFO_ENDPOINT',
                                  'https://{AUTH0_DOMAIN}/userinfo')
    headers = {'Authorization': f'Bearer {access_token}'}
    resp = requests.get(PROVIDER_USERINFO.format(AUTH0_DOMAIN=os.getenv('AUTH0_DOMAIN')),
                        headers=headers)
    resp.raise_for_status()
    return resp.json()

# Simple helper used by login flow
if __name__ == '__main__':
    sample_jwt = os.getenv('SAMPLE_JWT')  # fill in a JWT for testing
    if sample_jwt:
        claims = verify_id_token(sample_jwt, audience='YOUR_AUDIENCE')
        print('Normalized claims:', claims)
