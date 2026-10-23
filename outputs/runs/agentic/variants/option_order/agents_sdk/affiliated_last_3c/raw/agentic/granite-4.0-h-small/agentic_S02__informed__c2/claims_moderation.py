import json
from typing import List, Dict

def moderate_free_text_claims(claims: Dict[str, str]) -> Dict[str, str]:
    """Simple rule‑based moderation of arbitrary free‑text OIDC claims.

    The function checks each claim for disallowed content (e.g., hate speech, profanity).
    In a real deployment you would replace the naive checks with a call to a hosted
    content‑moderation service such as Alibaba Content Moderation or Perspective API.
    """
    MODERATION_RULES = [
        (r'\b(?:hate|kill|bomb)\b', 'PROHIBITED'),          # example regexes
        (r'\b(?:sex|nude)\b', 'PROHIBITED'),
        (r'\b(?:password|secret|creds)\b', 'SENSITIVE'),
    ]

    moderated = {}
    for key, value in claims.items():
        allowed = True
        rationale = None
        for pattern, label in MODERATION_RULES:
            if isinstance(value, str) and pattern.search(value):
                allowed = False
                rationale = label
                break
        if allowed:
            moderated[key] = value
        else:
            moderated[f'flagged_{key}'] = value  # keep for audit but flag
    return moderated

if __name__ == '__main__':
    # Example input: a raw ID token payload
    sample_payload = {
        'sub': 'user123',
        'name': 'John Doe',
        'email': 'john@example.com',
        'bio': 'I love bombarding the city with fireworks',   # contains a prohibited word
        'favorite_color': 'blue'
    }
    clean = moderate_free_text_claims(sample_payload)
    print('Moderated claims:', json.dumps(clean, indent=2))
