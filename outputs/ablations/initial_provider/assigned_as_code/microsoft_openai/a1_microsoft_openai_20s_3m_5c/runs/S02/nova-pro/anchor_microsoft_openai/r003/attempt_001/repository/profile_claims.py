import msal

from identity_client import get_identity_client


def fetch_profile_claims(access_token):
    client = get_identity_client()
    result = client.acquire_token_silent(scopes=['User.Read'], token_cache={})
    if 'access_token' in result:
        graph_data = client.get('https://graph.microsoft.com/v1.0/me', headers={'Authorization': f'Bearer {result['access_token']}'})
        return graph_data.json()
    return None