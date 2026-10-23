import msal

def fetch_profile_claims(access_token):
    graph_client = msal.ConfidentialClientApplication(
        client_id="your-client-id",
        authority="https://login.microsoftonline.com/your-tenant-id",
        client_credential="your-client-secret"
    )
    result = graph_client.acquire_token_silent(["user.read"], account=None)
    if "access_token" in result:
        headers = {'Authorization': 'Bearer ' + result['access_token']}
        response = requests.get('https://graph.microsoft.com/v1.0/me', headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error: {response.status_code}")
    else:
        print(result.get("error"))
    return None