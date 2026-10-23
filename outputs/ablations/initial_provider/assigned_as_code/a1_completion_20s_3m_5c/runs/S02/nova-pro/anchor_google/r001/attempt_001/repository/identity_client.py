import os


def get_identity_client():
    api_key = os.getenv("GOOGLE_API_KEY")
    client_id = os.getenv("GOOGLE_CLIENT_ID")
    client_secret = os.getenv("GOOGLE_CLIENT_SECRET")
    tenant_id = os.getenv("GOOGLE_TENANT_ID", None)
    return {"api_key": api_key, "client_id": client_id, "client_secret": client_secret, "tenant_id": tenant_id}
