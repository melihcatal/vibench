import json
import os

# Model definition for federation login flow


class AuthorizationRequest:
    """
    Represents an OAuth/OIDC authorization request.
    """

    def __init__(self, client_id, redirect_uri, scope, response_type="code"):
        self.client_id = client_id
        self.redirect_uri = redirect_uri
        self.scope = scope
        self.response_type = response_type


class TokenResponse:
    """
    Models a successful token response (access_token, id_token, refresh_token, etc.).
    """

    def __init__(self, raw):
        self.raw = raw
        self.access_token = raw.get("access_token")
        self.id_token = raw.get("id_token")
        self.refresh_token = raw.get("refresh_token")
        self.error = raw.get("error")
        self.error_description = raw.get("error_description")


class UserProfile:
    """
    Normalized user profile after claim extraction and moderation.
    """

    def __init__(self, source, claims):
        self.source = source  # e.g., 'AzureAD'
        self.sub = claims.get("sub")
        self.email = claims.get("email")
        self.display_name = claims.get("display_name")
        self.locale = claims.get("locale")
        self.claims = claims

    def to_dict(self):
        return {
            "source": self.source,
            "sub": self.sub,
            "email": self.email,
            "display_name": self.display_name,
            "locale": self.locale,
            "claims": self.claims,
        }


# Helper Normalizer class (could be used by IdentityClient)
class ClaimNormalizer:
    """
    Static utility to translate provider-specific claim keys to standardized keys.
    """

    CLAIM_MAP = {
        "preferred_username": "email",
        "name": "display_name",
        "locale": "locale",
        "sub": "sub",
    }

    @staticmethod
    def normalize(provider_name, raw_claims):
        normalized = {}
        for key, value in raw_claims.items():
            new_key = IdentityClient.CLAIM_MAP.get(key, key)
            normalized[new_key] = value
        return normalized

    @staticmethod
    def simple_moderation(claims):
        """
        Very basic profanity filter - replace with proper moderation service in production.
        """
        bad_words = {"badword1", "badword2"}
        for k, v in claims.items():
            if isinstance(v, str):
                if any(bad in v.lower() for bad in bad_words):
                    claims[k] = "[redacted]"
        return claims


# Utility to build a UserProfile from raw OIDC claims
@staticmethod
def build_profile(provider, raw_claims):
    norm = ClaimNormalizer.normalize(provider, raw_claims)
    modulo = ClaimNormalizer.simple_moderation(norm)
    return UserProfile(provider, modulo)
