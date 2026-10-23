import os
from typing import Optional
from supabase import create_client, Client

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")


def get_identity_client() -> Client:
    """Initialize and return a Supabase client for identity operations."""
    if not SUPABASE_URL or not SUPABASE_KEY:
        raise ValueError("Supabase URL and Key must be set in environment variables")
    
    return create_client(SUPABASE_URL, SUPABASE_KEY)


def get_user_locale(user_id: str) -> Optional[str]:
    """Fetch the user's locale from Supabase."""
    supabase = get_identity_client()
    response = supabase.table("users").select("locale").eq("id", user_id).execute()
    if response.data:
        return response.data[0].get("locale")
    return None