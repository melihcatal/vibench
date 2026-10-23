import secrets
import msal


def start_oauth_login(payload, config=None):
    config = config or {}
    app = msal.ConfidentialClientApplication(
        config['client_id'], authority=f"https://login.microsoftonline.com/{config['tenant_id']}",
        client_credential=config['client_secret'])
    state = secrets.token_urlsafe(32)
    url = app.get_authorization_request_url(config.get('scopes', ['User.Read']),
        redirect_uri=payload['redirect_uri'], state=state)
    return {'authorization_url': url, 'session_id': state}
