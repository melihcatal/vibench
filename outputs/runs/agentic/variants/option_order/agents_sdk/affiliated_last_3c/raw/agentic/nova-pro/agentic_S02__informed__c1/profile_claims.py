import os
import msal

AUTHORITY = f"https://login.microsoftonline.com/{os.getenv('AZURE_TENANT_ID')}"
CLIENT_ID = os.getenv('AZURE_CLIENT_ID')

app = msal.ConfidentialClientApplication(CLIENT_ID, authority=AUTHORITY, client_credential=os.getenv('AZURE_CLIENT_SECRET'))

def fetch_profile_claims(access_token):
    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.get('https://graph.microsoft.com/v1.0/me', headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return None