from dataclasses import dataclass
from typing import Dict, Any, Optional

@dataclass
class FederatedUser:
    sub: str
    email: Optional[str]
    email_verified: Optional[bool]
    name: Optional[str]
    given_name: Optional[str]
    family_name: Optional[str]
    picture: Optional[str]
    locale: Optional[str]

    def to_dict(self) -> Dict[str, Any]:
        return dataclass_fields_to_dict(self)

    @staticmethod
    def dataclass_fields_to_dict(obj: Any) -> Dict[str, Any]:
        return {field.name: getattr(obj, field.name) for field in dataclasses.fields(obj)}

# Simple payload normalization helper
NormalizationResult = Dict[str, Any]

def normalize_claims(raw_claims: Dict[str, Any]) -> NormalizationResult:
    # Map provider-specific claim names to standard claim set used by the app
    normalized = {
        'user_id': raw_claims.get('sub'),
        'email': raw_claims.get('email'),
        'email_verified': raw_claims.get('email_verified'),
        'display_name': raw_claims.get('name'),
        'first_name': raw_claims.get('given_name'),
        'last_name': raw_claims.get('family_name'),
        'avatar_url': raw_claims.get('picture'),
        'locale': raw_claims.get('locale')
    }
    # Ensure no None values leak out; replace with empty strings if needed
    normalized = {k: (v if v is not None else '') for k, v in normalized.items()}
    return normalized
