from typing import List, Optional
from identity_models import FederatedProfile

# Simple moderation rules – reject claims containing prohibited keywords
PROHIBITED_KEYWORDS = ['hate', 'offensive', 'spam']

def moderate_claims(profile: FederatedProfile, claims: dict) -> dict:
    '''Remove or sanitize any claim that contains a prohibited keyword.'''
    moderated = {}
    for key, value in claims.items():
        if isinstance(value, str) and any(kw.lower() in value.lower() for kw in PROHIBITED_KEYWORDS):
            print(f'Claim {key} contains prohibited content; sanitizing.')
            moderated[key] = '[REDACTED]'
        else:
            moderated[key] = value
    # Merge back into the normalized profile
    profile.dict().update(moderated)
    return profile

if __name__ == '__main__':
    # Example with a mock profile + raw claims from a provider
    raw_claims = {
        'nickname': 'happy_user',
        'bio': 'I love coding and spreading peace',
        'notes': 'This is a hateful message about opponents',  # contains 'hate'
    }
    profile = FederatedProfile(
        sub='12345',
        name='John Doe',
        email='john@example.com',
        picture='http://example.com/avatar.png',
        email_verified=True,
    )
    moderated = moderate_claims(profile, raw_claims)
    print('Moderated claims:', moderated.dict())
