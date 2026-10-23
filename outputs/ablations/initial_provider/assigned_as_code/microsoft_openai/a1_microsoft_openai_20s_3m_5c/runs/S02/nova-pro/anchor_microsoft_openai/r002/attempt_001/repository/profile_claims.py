import msal


def fetch_profile_claims(access_token, config):
    app = msal.ConfidentialClientApplication(
        config['client_id'], authority=f"https://login.microsoftonline.com/{config['tenant_id']}",
        client_credential=config['client_secret'])
    graph_data = app.acquire_token_silent(['User.Read'], account=None)
    if graph_data and 'access_token' in graph_data:
        graph_client = msal.GraphClient(access_token=graph_data['access_token'])
        user_profile = graph_client.get('/me')
        return user_profile
    return None