from typing import Dict, Any


def normalize_profile_claims(claims: Dict[str, Any]) -> Dict[str, Any]:
    return {"email": claims["email"], "name": claims["name"]}
