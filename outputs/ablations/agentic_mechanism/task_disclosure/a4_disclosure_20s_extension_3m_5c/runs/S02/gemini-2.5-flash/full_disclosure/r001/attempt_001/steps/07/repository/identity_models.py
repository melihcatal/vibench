
class FederatedLoginRequest:
    """
    Represents a request for a federated login flow.
    """
    def __init__(self, provider: str, redirect_uri: str, state: str = None, nonce: str = None):
        self.provider = provider
        self.redirect_uri = redirect_uri
        self.state = state
        self.nonce = nonce

    def to_dict(self):
        return {
            "provider": self.provider,
            "redirect_uri": self.redirect_uri,
            "state": self.state,
            "nonce": self.nonce,
        }

class FederatedLoginResponse:
    """
    Represents a response from a federated login flow.
    """
    def __init__(self, access_token: str, id_token: str = None, refresh_token: str = None,
                 token_type: str = "Bearer", expires_in: int = None, scope: str = None):
        self.access_token = access_token
        self.id_token = id_token
        self.refresh_token = refresh_token
        self.token_type = token_type
        self.expires_in = expires_in
        self.scope = scope

    def to_dict(self):
        return {
            "access_token": self.access_token,
            "id_token": self.id_token,
            "refresh_token": self.refresh_token,
            "token_type": self.token_type,
            "expires_in": self.expires_in,
            "scope": self.scope,
        }

class UserProfileClaims:
    """
    Represents normalized user profile claims after federated login.
    """
    def __init__(self, user_id: str, email: str = None, name: str = None,
                 given_name: str = None, family_name: str = None, picture: str = None):
        self.user_id = user_id
        self.email = email
        self.name = name
        self.given_name = given_name
        self.family_name = family_name
        self.picture = picture

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "email": self.email,
            "name": self.name,
            "given_name": self.given_name,
            "family_name": self.family_name,
            "picture": self.picture,
        }

class ClaimNormalizer:
    """
    Helper for normalizing claims from various identity providers.
    """
    @staticmethod
    def normalize_claims(raw_claims: dict) -> UserProfileClaims:
        """
        Normalizes raw claims from an identity provider into a standardized UserProfileClaims object.
        This is a placeholder and should be implemented with actual normalization logic.
        """
        user_id = raw_claims.get("sub") or raw_claims.get("id")
        email = raw_claims.get("email")
        name = raw_claims.get("name")
        given_name = raw_claims.get("given_name") or raw_claims.get("first_name")
        family_name = raw_claims.get("family_name") or raw_claims.get("last_name")
        picture = raw_claims.get("picture") or raw_claims.get("profile_image")

        if not user_id:
            raise ValueError("Could not extract user ID from raw claims.")

        return UserProfileClaims(
            user_id=str(user_id),
            email=email,
            name=name,
            given_name=given_name,
            family_name=family_name,
            picture=picture
        )
