import os
from dataclasses import dataclass
from typing import Dict, Optional

from google.cloud import firestore


@dataclass
class IdentityProviderConfig:
    provider_domain: str
    tenant_id: str
    client_id: str
    client_secret: str
    redirect_uri: str
    default_scope: str


@dataclass
class PKCEState:
    state: str
    nonce: Optional[str]
    code_verifier: str


_STATE_CACHE: Dict[str, PKCEState] = {}


def get_identity_provider_config() -> IdentityProviderConfig:
    return IdentityProviderConfig(
        provider_domain=os.environ["AUTH0_DOMAIN"],
        tenant_id=os.environ.get("AZURE_TENANT_ID", "common"),
        client_id=os.environ["OIDC_CLIENT_ID"],
        client_secret=os.environ.get("OIDC_CLIENT_SECRET", ""),
        redirect_uri=os.environ["OIDC_REDIRECT_URI"],
        default_scope=os.environ.get("OIDC_SCOPE", "openid profile email"),
    )


def store_pkce_state(state: str, nonce: Optional[str], code_verifier: str) -> None:
    _STATE_CACHE[state] = PKCEState(state=state, nonce=nonce, code_verifier=code_verifier)


def load_pkce_state(state: str) -> PKCEState:
    return _STATE_CACHE.get(state, PKCEState(state=state, nonce=None, code_verifier=""))


def get_firestore_client() -> firestore.Client:
    return firestore.Client(project=os.environ.get("GOOGLE_CLOUD_PROJECT"))
