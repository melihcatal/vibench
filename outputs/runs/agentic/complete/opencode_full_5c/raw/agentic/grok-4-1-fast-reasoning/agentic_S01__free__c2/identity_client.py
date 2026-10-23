import os


def get_supabase_config() -> dict:
    url = os.getenv("SUPABASE_URL")
    anon_key = os.getenv("SUPABASE_ANON_KEY")
    if not url or not anon_key:
        raise ValueError("Supabase URL and anon key are required")
    return {"url": url, "key": anon_key}
