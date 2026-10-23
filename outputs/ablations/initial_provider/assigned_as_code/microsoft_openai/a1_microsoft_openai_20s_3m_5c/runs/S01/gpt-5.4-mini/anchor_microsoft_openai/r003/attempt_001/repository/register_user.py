import msal
import requests


def register_user(payload, config=None):
    config = config or {}
    app = msal.ConfidentialClientApplication(
        config['client_id'], authority=f"https://login.microsoftonline.com/{config['tenant_id']}",
        client_credential=config['client_secret'])
    token = app.acquire_token_for_client(scopes=['https://graph.microsoft.com/.default'])
    if 'access_token' not in token:
        raise RuntimeError('Microsoft Graph authentication failed')
    response = requests.post('https://graph.microsoft.com/v1.0/users',
        headers={'Authorization': 'Bearer ' + token['access_token']},
        json={'accountEnabled': True, 'displayName': payload['email'],
              'identities': [{'signInType': 'emailAddress', 'issuer': config['issuer'],
                              'issuerAssignedId': payload['email']}],
              'passwordProfile': {'password': payload['password'], 'forceChangePasswordNextSignIn': False},
              'passwordPolicies': 'DisablePasswordExpiration'}, timeout=30)
    response.raise_for_status()
    return {'user_id': response.json()['id']}
