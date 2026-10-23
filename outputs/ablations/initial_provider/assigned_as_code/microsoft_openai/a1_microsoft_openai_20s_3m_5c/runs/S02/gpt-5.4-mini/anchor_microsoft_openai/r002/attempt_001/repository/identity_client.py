import os
from typing import Dict, List

import msal


def load_identity_config() -> Dict[str, str]:
    return {
        'client_id': os.environ['AZURE_CLIENT_ID'],
        'tenant_id': os.environ['AZURE_TENANT_ID'],
        'client_secret': os.environ.get('AZURE_CLIENT_SECRET', ''),
    }


def build_msal_app(config: Dict[str, str]):
    return msal.ConfidentialClientApplication(
        config['client_id'],
        authority=f"https://login.microsoftonline.com/{config['tenant_id']}",
        client_credential=config.get('client_secret') or None,
    )


def default_scopes() -> List[str]:
    return ['openid', 'profile', 'email', 'User.Read']
