import msal

def start_oauth_login(authority, client_id, redirect_uri, scopes):
    app = msal.PublicClientApplication(
        client_id, authority=authority
    )
    flow = app.initiate_auth_code_flow(scopes, redirect_uri=redirect_uri)
    return flow['auth_uri']