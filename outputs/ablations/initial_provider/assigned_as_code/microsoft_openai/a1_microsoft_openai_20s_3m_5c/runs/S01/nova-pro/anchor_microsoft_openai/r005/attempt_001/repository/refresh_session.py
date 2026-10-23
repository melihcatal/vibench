import msal

def refresh_session(refresh_token, config=None):
    config = config or {}
    app = msal.ConfidentialClientApplication(
        config['client_id'], authority=f"https://login.microsoftonline.com/{config['tenant_id']}",
        client_credential=config['client_secret'])
    result = app.acquire_token_by_refresh_token(
        refresh_token, scopes=['https://graph.microsoft.com/.default'])
    if 'access_token' not in result:
        raise RuntimeError('Microsoft Graph token refresh failed')
    return result