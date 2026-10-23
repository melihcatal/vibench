from supabase import create_client, Client
from identity_client import SUPABASE_URL, SUPABASE_ANON_KEY

def password_reset(email: str, redirect_to: str = None) -> None:
    client: Client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)
    client.auth.reset_password_for_email(email, redirect_to=redirect_to)
