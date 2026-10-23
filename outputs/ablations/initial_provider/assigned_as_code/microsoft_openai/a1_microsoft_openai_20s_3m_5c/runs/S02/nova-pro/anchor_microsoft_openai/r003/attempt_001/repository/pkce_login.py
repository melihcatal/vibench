import msal

from identity_client import get_identity_client


def pkce_login(payload):
    client = get_identity_client()
    code_verifier = secrets.token_urlsafe(32)
    code_challenge = msal.ClientApplication('').create_code_challenge(code_verifier)
    result = client.initiate_device_flow(scopes=payload['scopes'], code_challenge=code_challenge)
    if 'device_code' in result:
        return {'device_code': result['device_code'], 'user_code': result['user_code'], 'verification_uri': result['verification_uri']}
    return None