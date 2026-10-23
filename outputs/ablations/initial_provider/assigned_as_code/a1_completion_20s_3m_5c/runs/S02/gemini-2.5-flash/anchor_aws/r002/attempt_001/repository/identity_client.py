import os
from typing import Dict, Any

from identity_models import FederatedLoginConfig, PkceLoginConfig

def load_federated_login_config() -> FederatedLoginConfig:
    return FederatedLoginConfig(
        domain=os.environ.get("AUTH0_DOMAIN", "YOUR_AUTH0_DOMAIN"),
        client_id=os.environ.get("AUTH0_CLIENT_ID", "YOUR_AUTH0_CLIENT_ID"),
        client_secret=os.environ.get("AUTH0_CLIENT_SECRET", "YOUR_AUTH0_CLIENT_SECRET"),
        redirect_uri=os.environ.get("AUTH0_CALLBACK_URL", "http://localhost:3000/callback"),
        audience=os.environ.get("AUTH0_AUDIENCE", None),
        scope=os.environ.get("AUTH0_SCOPE", "openid profile email")
    )

def load_pkce_login_config() -> PkceLoginConfig:
    return PkceLoginConfig(
        domain=os.environ.get("AUTH0_DOMAIN", "YOUR_AUTH0_DOMAIN"),
        client_id=os.environ.get("AUTH0_CLIENT_ID_PKCE", "YOUR_AUTH0_CLIENT_ID_PKCE"),
        redirect_uri=os.environ.get("AUTH0_CALLBACK_URL_PKCE", "http://localhost:3000/callback-pkce"),
        audience=os.environ.get("AUTH0_AUDIENCE", None),
        scope=os.environ.get("AUTH0_SCOPE", "openid profile email")
    )

def normalize_claims(raw_claims: Dict[str, Any]) -> Dict[str, Any]:
    # Basic normalization for Auth0 claims to a more generic format if needed
    # For this example, we'll return the raw claims directly.
    return raw_claims
