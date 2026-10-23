import os
import msal
import requests

class MicrosoftGraphClient:
    def __init__(self, tenant_id: str, client_id: str, client_secret: str):
        self.tenant_id = tenant_id
        self.client_id = client_id
        self.client_secret = client_secret
        self.authority = f"https://login.microsoftonline.com/{self.tenant_id}"
        self.app = msal.ConfidentialClientApplication(
            self.client_id, authority=self.authority, client_credential=self.client_secret
        )
        self.graph_api_endpoint = "https://graph.microsoft.com/v1.0"

    def _acquire_token(self):
        # For client credentials flow, scope is always .default
        token = self.app.acquire_token_for_client(scopes=["https://graph.microsoft.com/.default"])
        if "access_token" not in token:
            raise RuntimeError("Microsoft Graph authentication failed")
        return token["access_token"]

    def get_headers(self):
        access_token = self._acquire_token()
        return {'Authorization': 'Bearer ' + access_token, 'Content-Type': 'application/json'}

    def get(self, path: str):
        headers = self.get_headers()
        response = requests.get(f"{self.graph_api_endpoint}/{path}", headers=headers, timeout=30)
        response.raise_for_status()
        return response.json()

    def post(self, path: str, json_data: dict):
        headers = self.get_headers()
        response = requests.post(f"{self.graph_api_endpoint}/{path}", headers=headers, json=json_data, timeout=30)
        response.raise_for_status()
        return response.json()

    def patch(self, path: str, json_data: dict):
        headers = self.get_headers()
        response = requests.patch(f"{self.graph_api_endpoint}/{path}", headers=headers, json=json_data, timeout=30)
        response.raise_for_status()
        return response.json()

def get_microsoft_graph_client():
    tenant_id = os.environ.get("MS_TENANT_ID")
    client_id = os.environ.get("MS_CLIENT_ID")
    client_secret = os.environ.get("MS_CLIENT_SECRET")

    if not all([tenant_id, client_id, client_secret]):
        raise ValueError("Missing one or more Microsoft Graph environment variables: MS_TENANT_ID, MS_CLIENT_ID, MS_CLIENT_SECRET")

    return MicrosoftGraphClient(tenant_id, client_id, client_secret)
