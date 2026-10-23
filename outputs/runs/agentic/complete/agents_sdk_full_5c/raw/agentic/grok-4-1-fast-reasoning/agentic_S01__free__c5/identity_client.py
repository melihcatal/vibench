import os
from supabase import create_client, Client

def get_supabase_client() -> Client:
    url: str = os.getenv("SUPABASE_URL")
    key: str = os.getenv("SUPABASE_ANON_KEY")
    if not url or not key:
        raise ValueError("Missing SUPABASE_URL or SUPABASE_ANON_KEY")
    return create_client(url, key)