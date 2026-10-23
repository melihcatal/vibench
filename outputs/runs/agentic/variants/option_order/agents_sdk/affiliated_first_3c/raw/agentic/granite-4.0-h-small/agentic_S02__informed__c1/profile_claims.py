import json
from identity_models import FederatedProfile

def normalize_claims(jwt_claims, provider='cognito'):
    """Map raw JWT claims to a consistent FederatedProfile structure."""
    # Sample mapping for Amazon Cognito; add conditional logic for other providers if needed
    given_name = jwt_claims.get('given_name')
    family_name = jwt_claims.get('family_name')
    email = jwt_claims.get('email')
    phone_number = jwt_claims.get('phone_number')
    picture = jwt_claims.get('picture')
    sub = jwt_claims.get('sub')
    # Example of adding issuer & audience for audit later
    issuer = jwt_claims.get('iss')
    audience = jwt_claims.get('aud')
    profile = FederatedProfile(
        sub=sub,
        email=email,
        given_name=given_name,
        family_name=family_name,
        phone_number=phone_number,
        picture=picture,
        provider=provider,
        issuer=issuer,
        audience=audience,
    )
    return profile

# Example usage (outside request flow)
# raw = json.loads(open('token.json').read())
# profile = normalize_claims(raw)
# print(profile.dict())
