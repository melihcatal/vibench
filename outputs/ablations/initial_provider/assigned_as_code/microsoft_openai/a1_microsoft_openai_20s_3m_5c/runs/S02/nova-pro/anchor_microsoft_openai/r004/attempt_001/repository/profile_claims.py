import msal

def get_profile_claims(access_token):
    graph_client = msal.ConfidentialClientApplication(
        '00000000-0000-0000-0000-000000000000', authority='https://graph.microsoft.com',
        token=access_token)
    result = graph_client.acquire_token_silent(['User.Read'], account=None)
    if 'access_token' in result:
        profile = graph_client.get('https://graph.microsoft.com/v1.0/me')
        return profile.json()
    return None