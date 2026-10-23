from typing import Optional, Dict, Any
from dataclasses import dataclass

@dataclass
class FederatedTokens:
    access_token: str
    token_type: str
    expires_in: int
    refresh_token: Optional[str] = None
    id_token: Optional[str] = None
    scope: Optional[str] = None

@dataclass
class UserProfileClaims:
    id: Optional[str]
    email: Optional[str]
    name: Optional[str]
    given_name: Optional[str]
    family_name: Optional[str]
    picture: Optional[str]
    # Add other common claims as needed
    raw_claims: Optional[Dict[str, Any]] = None # To store the original claims from the IdP

@dataclass
class AuditRecord:
    timestamp: str # ISO 8601 format
    event_type: str # e.g., "LOGIN_SUCCESS", "LOGIN_FAILURE", "TOKEN_REFRESH"
    user_id: Optional[str]
    provider: str # e.g., "Google", "Okta"
    details: Dict[str, Any]
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None

def normalize_profile_claims(provider: str, raw_claims: Dict[str, Any]) -> UserProfileClaims:
    """Normalizes raw claims from an identity provider into a common UserProfileClaims structure."""
    if provider == "Google":
        # This should align with the normalization in profile_claims.py
        normalized = {
            "id": raw_claims.get("resourceName", "").split('/')[-1] if raw_claims.get("resourceName") else None,
            "email": None,
            "name": None,
            "given_name": None,
            "family_name": None,
            "picture": None,
        }

        if raw_claims.get("emailAddresses"):
            for email_entry in raw_claims["emailAddresses"]:
                if email_entry.get("metadata", {}).get("primary"):
                    normalized["email"] = email_entry.get("value")
                    break
            if not normalized["email"] and raw_claims["emailAddresses"]:
                normalized["email"] = raw_claims["emailAddresses"][0].get("value")

        if raw_claims.get("names"):
            for name_entry in raw_claims["names"]:
                if name_entry.get("metadata", {}).get("primary"):
                    normalized["name"] = name_entry.get("displayName")
                    normalized["given_name"] = name_entry.get("givenName")
                    normalized["family_name"] = name_entry.get("familyName")
                    break
            if not normalized["name"] and raw_claims["names"]:
                normalized["name"] = raw_claims["names"][0].get("displayName")
                normalized["given_name"] = raw_claims["names"][0].get("givenName")
                normalized["family_name"] = raw_claims["names"][0].get("familyName")

        if raw_claims.get("photos"):
            for photo_entry in raw_claims["photos"]:
                if photo_entry.get("metadata", {}).get("primary"):
                    normalized["picture"] = photo_entry.get("url")
                    break
            if not normalized["picture"] and raw_claims["photos"]:
                normalized["picture"] = raw_claims["photos"][0].get("url")

        return UserProfileClaims(**normalized, raw_claims=raw_claims)

    elif provider == "Okta":
        # Assuming ID token claims or userinfo endpoint response from Okta
        return UserProfileClaims(
            id=raw_claims.get("sub"), # 'sub' is standard for user ID
            email=raw_claims.get("email"),
            name=raw_claims.get("name"),
            given_name=raw_claims.get("given_name"),
            family_name=raw_claims.get("family_name"),
            picture=raw_claims.get("picture"),
            raw_claims=raw_claims
        )
    else:
        # Fallback for unknown providers, or minimal parsing
        return UserProfileClaims(
            id=raw_claims.get("sub") or raw_claims.get("id"),
            email=raw_claims.get("email"),
            name=raw_claims.get("name") or raw_claims.get("displayName"),
            raw_claims=raw_claims
        )

if __name__ == "__main__":
    # Example Google raw claims (simplified)
    google_raw_claims_example = {
        "resourceName": "people/12345",
        "emailAddresses": [{
            "value": "test@example.com",
            "metadata": {"primary": True}
        }],
        "names": [{
            "displayName": "John Doe",
            "givenName": "John",
            "familyName": "Doe",
            "metadata": {"primary": True}
        }],
        "photos": [{
            "url": "https://lh3.googleusercontent.com/a/image.jpg",
            "metadata": {"primary": True}
        }]
    }
    google_profile = normalize_profile_claims("Google", google_raw_claims_example)
    print("Normalized Google Profile:", google_profile)

    # Example Okta raw claims (simplified)
    okta_raw_claims_example = {
        "sub": "okta_user_id_789",
        "name": "Jane Smith",
        "email": "jane.smith@okta.com",
        "given_name": "Jane",
        "family_name": "Smith",
        "picture": "https://okta.com/profile.jpg"
    }
    okta_profile = normalize_profile_claims("Okta", okta_raw_claims_example)
    print("Normalized Okta Profile:", okta_profile)
