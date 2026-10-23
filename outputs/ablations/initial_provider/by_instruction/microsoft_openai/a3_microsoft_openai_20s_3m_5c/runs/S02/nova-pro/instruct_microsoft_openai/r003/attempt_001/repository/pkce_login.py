import msal

def pkce_login(authority, client_id, redirect_uri, scopes):
    app = msal.PublicClientApplication(
        client_id, authority=authority
    )
    flow = app.initiate_auth_code_flow(scopes, redirect_uri=redirect_uri, code_challenge_method='S256')
    return flow['auth_uri']