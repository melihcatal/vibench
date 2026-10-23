import os
from dataclasses import dataclass


@dataclass
class IdentityConfig:
    tenant_id: str
    client_id: str
    client_secret: str
    issuer: str
    openai_api_key: str = ''
    pinecone_api_key: str = ''
    pinecone_index: str = ''


def load_identity_config(config=None):
    config = config or {}
    return IdentityConfig(
        tenant_id=config.get('tenant_id') or os.environ['AZURE_TENANT_ID'],
        client_id=config.get('client_id') or os.environ['AZURE_CLIENT_ID'],
        client_secret=config.get('client_secret') or os.environ['AZURE_CLIENT_SECRET'],
        issuer=config.get('issuer') or os.environ['AZURE_B2C_ISSUER'],
        openai_api_key=config.get('openai_api_key') or os.environ.get('OPENAI_API_KEY', ''),
        pinecone_api_key=config.get('pinecone_api_key') or os.environ.get('PINECONE_API_KEY', ''),
        pinecone_index=config.get('pinecone_index') or os.environ.get('PINECONE_INDEX', ''),
    )


def identity_settings(config=None):
    loaded = load_identity_config(config)
    return {
        'tenant_id': loaded.tenant_id,
        'client_id': loaded.client_id,
        'client_secret': loaded.client_secret,
        'issuer': loaded.issuer,
        'openai_api_key': loaded.openai_api_key,
        'pinecone_api_key': loaded.pinecone_api_key,
        'pinecone_index': loaded.pinecone_index,
    }
