from identity_client import get_identity_client


def fetch_profile_claims(access_token):
    app = get_identity_client()
    result = app.acquire_token_silent(['User.Read'], account=app.get_account(access_token))
    if 'access_token' in result:
        graph_data = requests.get(  # Using Microsoft Graph API
            'https://graph.microsoft.com/v1.0/me',
            headers={'Authorization': 'Bearer ' + result['access_token']},
        ).json()
        return graph_data
    return None