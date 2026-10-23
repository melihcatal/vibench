import requests
from identity_client import pkce_pair, load_identity_config


def pkce_login(payload, config=None):
    config = load_identity_config(config)
    verifier, challenge = pkce_pair()
    request = {
        "providerId": config["provider_id"],
        "continueUri": payload["redirect_uri"],
        "codeChallenge": challenge,
        "codeChallengeMethod": "S256",
    }
    if config.get("tenant_id"):
        request["tenantId"] = config["tenant_id"]
    response = requests.post(
        "https://identitytoolkit.googleapis.com/v1/accounts:createAuthUri",
        params={"key": config["api_key"]},
        json=request,
        timeout=30,
    )
    response.raise_for_status()
    result = response.json()
    result["code_verifier"] = verifier
    result["authorization_url"] = result.get("authUri")
    return result
