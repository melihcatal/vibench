from supabase import create_client, Client
from identity_client import SUPABASE_URL, SUPABASE_ANON_KEY
from identity_models import Session

def refresh_session(refresh_token: str) -> tuple[str | None, str | None]:
    client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)
    response = client.auth.refresh_session({"refresh_token": refresh_token})
    session: Session = response.get("session", {})
    if session:
        return session["access_token"], session["refresh_token"]
    return None, None
