from supabase import create_client, Client
from identity_client import SUPABASE_URL, SUPABASE_ANON_KEY
from identity_models import AuthPayload, AuthResponse

def register_user(email: str, password: str) -> str:
    client: Client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)
    payload: AuthPayload = {"email": email, "password": password}
    response: AuthResponse = client.auth.sign_up(payload)
    return response["user"]["id"] if response.get("user") else None
