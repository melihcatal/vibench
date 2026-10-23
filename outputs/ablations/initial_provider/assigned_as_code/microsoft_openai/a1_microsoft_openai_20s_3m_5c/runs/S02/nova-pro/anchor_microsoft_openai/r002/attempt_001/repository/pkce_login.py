import msal
import secrets


def pkce_login(payload, config=None):
    config = config or {}
    app = msal.PublicClientApplication(
        config['client_id'], authority=f"https://login.microsoftonline.com/{config['tenant_id']}")
    code_verifier = secrets.token_urlsafe(32)
    code_challenge = msal.create_code_challenge(code_verifier)
    flow = app.initiate_device_flow(scopes=config.get('scopes', ['User.Read']))
    if 'user_code' not in flow:
        raise ValueError('Failed to create device flow')
    print(f"User code: {flow['user_code']}")
    result = app.acquire_token_by_device_flow(flow, code_verifier=code_verifier)
    return result