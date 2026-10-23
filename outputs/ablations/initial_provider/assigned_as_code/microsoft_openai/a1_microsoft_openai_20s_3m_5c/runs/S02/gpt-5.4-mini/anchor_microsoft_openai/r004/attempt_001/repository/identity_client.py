import os
from dataclasses import dataclass

import msal


@dataclass
class IdentityConfig:
    client_id: str
    tenant_id: str
    client_secret: str | None = None
    authority_host: str = 'https://login.microsoftonline.com'
    scopes: list[str] | None = None
    redirect_uri: str | None = None


def load_identity_config(overrides=None):
    overrides = overrides or {}
    return IdentityConfig(
        client_id=overrides.get('client_id') or os.environ.get('AZURE_CLIENT_ID', ''),
        tenant_id=overrides.get('tenant_id') or os.environ.get('AZURE_TENANT_ID', ''),
        client_secret=overrides.get('client_secret') or os.environ.get('AZURE_CLIENT_SECRET'),
        authority_host=overrides.get('authority_host') or os.environ.get('AZURE_AUTHORITY_HOST', 'https://login.microsoftonline.com'),
        scopes=overrides.get('scopes') or ['User.Read'],
        redirect_uri=overrides.get('redirect_uri') or os.environ.get('AZURE_REDIRECT_URI'),
    )


def build_msal_app(config: IdentityConfig):
    if config.client_secret:
        return msal.ConfidentialClientApplication(
            config.client_id,
            authority=f'{config.authority_host}/{config.tenant_id}',
            client_credential=config.client_secret,
        )
    return msal.PublicClientApplication(
        config.client_id,
        authority=f'{config.authority_host}/{config.tenant_id}',
    )
