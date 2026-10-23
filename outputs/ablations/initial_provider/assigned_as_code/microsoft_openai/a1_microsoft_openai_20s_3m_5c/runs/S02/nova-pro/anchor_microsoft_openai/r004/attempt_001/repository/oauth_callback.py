import msal

def exchange_code_for_tokens(code, config):
    app = msal.ConfidentialClientApplication(
        config['client_id'], authority=f"https://login.microsoftonline.com/{config['tenant_id']}",
        client_credential=config['client_secret'])
    result = app.acquire_token_by_authorization_code(
        code, scopes=config.get('scopes', ['User.Read']))
    return result