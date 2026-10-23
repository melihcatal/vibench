from dataclasses import dataclass, asdict
from typing import Mapping, Any

# Helper local file: identity_models.py
# Normalization helpers for federated login claims

@dataclass

class FederatedProfile:
    sub: str
    email: str
    given_name: str
    family_name: str
    preferred_username: str
    # Add more fields as needed

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]):
        return cls(
            sub=data.get("sub"),
            email=data.get("email"),
            given_name=data.get("given_name"),
            family_name=data.get("family_name"),
            preferred_username=data.get("preferred_username")
        )

    def to_dict(self) -> Mapping[str, Any]:
        return asdict(self)

# Example normalization function for different provider payloads
def normalize_claims(raw_claims: Mapping[str, Any]) -> FederatedProfile:
    # Map common claim names to our standard fields
    return FederatedProfile(
        sub=raw_claims.get("sub") or raw_claims.get("id"),
        email=raw_claims.get("email") or raw_claims.get("mail"),
        given_name=raw_claims.get("given_name") or raw_claims.get("givenName"),
        family_name=raw_claims.get("family_name") or raw_claims.get("familyName") or raw_claims.get("surname"),
        preferred_username=raw_claims.get("preferred_username") or raw_claims.get("userPrincipalName")
    )

if __name__ == "__main__":
    import json, sys
    raw = json.load(sys.stdin)
    norm = normalize_claims(raw)
    print(json.dumps(asdict(norm), indent=2))
