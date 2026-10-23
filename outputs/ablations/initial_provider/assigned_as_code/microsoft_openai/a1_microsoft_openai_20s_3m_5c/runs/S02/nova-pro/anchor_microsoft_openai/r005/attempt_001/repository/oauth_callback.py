import msal


def oauth_callback(payload, config=None):
    config = config or {}
    app = msal.ConfidentialClientApplication(
        config['client_id'], authority=f"https://login.microsoftonline.com/{config['tenant_id']}",
        client_credential=config['client_secret'])
    result = app.acquire_token_by_authorization_code(
        payload['code'], scopes=config.get('scopes', ['User.Read']),
        redirect_uri=payload['redirect_uri'])
    return result