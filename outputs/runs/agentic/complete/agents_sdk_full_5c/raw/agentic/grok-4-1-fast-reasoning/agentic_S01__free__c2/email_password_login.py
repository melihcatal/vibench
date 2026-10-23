from supabase import create_client, Client
from identity_client import SUPABASE_URL, SUPABASE_ANON_KEY
from identity_models import AuthPayload, AuthResponse

def email_password_login(email: str, password: str) -> tuple[str | None, str | None]:
    client: Client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)
    payload: AuthPayload = {"email": email, "password": password}
    response: AuthResponse = client.auth.sign_in_with_password(payload)
    session = response.get("session")
    if session:
        return session["access_token"], session["refresh_token"]
    return None, None
