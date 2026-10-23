import jwt
import base64
import hashlib
import urllib.parse
from typing import Any, Dict

# Utility to decode JWT without verification (useful for demos)
def decode_jwt(token: str) -> Dict[str, Any]:
    """Decode the JWT payload (claims) without verifying signature."""
    header, payload, sig = token.split(".")
    decoded = base64.urlsafe_b64decode(payload + "==")
    return jwt.json.loads(decoded)

# Simple JWT verification placeholder (replace with proper JWK fetch & verify in prod)

def verify_id_token(token: str, issuer: str, audience: str) -> Dict[str, Any]:
    # In real implementation fetch the JWKS from <issuer>/.well-known/jwks.json
    # and verify the signature using the appropriate key.
    payload = decode_jwt(token)
    # Simple checks
    assert payload["iss"] == issuer, "Invalid issuer"
    assert payload["aud"] == audience, "Invalid audience"
    assert not payload["exp"] < int(time.time()), "Token expired"
    return payload

# Normalized user profile class

class UserProfile:
    def __init__(self, sub: str, name: str, email: str, email_verified: bool,
                 locale: str = None, picture: str = None):
        self.sub = sub
        self.name = name
        self.email = email
        self.email_verified = email_verified
        self.locale = locale
        self.picture = picture

    @classmethod
    def from_google(cls, data: Dict[str, Any]) -> Any:
        # Google's tokeninfo / userinfo fields
        return cls(
            sub=data.get("sub"),
            name=data.get("name"),
            email=data.get("email"),
            email_verified=data.get("email_verified", False),
            locale=data.get("locale"),
            picture=data.get("picture")
        )

    @classmethod
    def from_auth0(cls, data: Dict[str, Any]) -> Any:
        # Auth0 userinfo fields
        return cls(
            sub=data.get("sub"),
            name=data.get("name"),
            email=data.get("email"),
            email_verified=data.get("email_verified", False),
            locale=data.get("locale"),
            picture=data.get("picture")
        )

    @classmethod
    def from_okta(cls, data: Dict[str, Any]) -> Any:
        # Okta userinfo fields
        return cls(
            sub=data.get("sub"),
            name=data.get("name"),
            email=data.get("email"),
            email_verified=data.get("emailVerified", False),
            locale=data.get("locale"),
            picture=data.get("profileImageUrl")
        )

# Helper to compute PKCE S256 challenge

def generate_pkce_pair() -> (str, str):
    """Create a PKCE code verifier and its SHA256 S256 challenge."""
    verifier = base64.urlsafe_b64encode(secrets.token_bytes(32)).decode().rstrip("=")
    hashed = hashlib.sha256(verifier.encode()).digest()
    challenge = base64.urlsafe_b64encode(hashed).decode().rstrip("=")
    return verifier, challenge

# Helper to build PKCE OAuth authorization URL (Google example)

def build_pkce_url(client_id: str, redirect_uri: str, scopes: list, issuer: str):
    verifier, challenge = generate_pkce_pair()
    params = {
        "client_id": client_id,
        "response_type": "code",
        "redirect_uri": redirect_uri,
        "scope": " ".join(scopes),
        "code_challenge": challenge,
        "code_challenge_method": "S256",
        "prompt": "consent"
    }
    return f"{issuer}?" + urllib.parse.urlencode(params), verifier

# Exported for the PKCE flow integration files
exported = {
    "decode_jwt": decode_jwt,
    "verify_id_token": verify_id_token,
    "UserProfile": UserProfile,
    "build_pkce_url": build_pkce_url,
    "generate_pkce_pair": generate_pkce_pair
}

if __name__ == "__main__":
    # simple demo
    pass
