from typing import Dict


def normalize_claims(claims: Dict[str, str]) -> Dict[str, str]:
    return {
        'sub': claims.get('sub', ''),
        'name': claims.get('name', ''),
        'email': claims.get('email', ''),
        'picture': claims.get('picture', '')
    }