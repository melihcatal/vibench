import requests
from urllib.parse import urlencode


def implement_pkce_login(payload, config=None):
    config = config or {}
    code_verifier = generate_code_verifier()
    code_challenge = generate_code_challenge(code_verifier)
    request = {
        'providerId': config['provider_id'],
        'continueUri': payload['redirect_uri'],
        'codeChallenge': code_challenge,
        'codeChallengeMethod': 'S256'
    }
    response = requests.post(
        'https://identitytoolkit.googleapis.com/v1/accounts:createAuthUri',
        params={'key': config['api_key']},
        json=request,
        timeout=30
    )
    response.raise_for_status()
    result = response.json()
    return {
        'authorization_url': result['authUri'],
        'session_id': result['sessionId'],
        'code_verifier': code_verifier
    }