from typing import Dict


def normalize_profile_claims(claims: Dict) -> Dict:
    return {
        "sub": claims["sub"],
        "name": claims["name"],
        "email": claims["email"],
        "picture": claims["picture"]
    }
