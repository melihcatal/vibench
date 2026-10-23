import json

import requests

from identity_client import discovery_document, load_oidc_config
from identity_models import normalize_claims


def fetch_profile(access_token: str) -> str:
    config = load_oidc_config()
    oidc = discovery_document(config.issuer)
    profile = requests.get(
        oidc["userinfo_endpoint"],
        headers={"Authorization": f"Bearer {access_token}"},
        timeout=15,
    ).json()
    return json.dumps(normalize_claims(profile))
