import os

from supabase import create_client


def store_profile_note(account_id: str, note: str, metadata: dict):
    url = os.environ["SUPABASE_URL"]
    key = os.environ["SUPABASE_SERVICE_ROLE_KEY"]
    client = create_client(url, key)
    return (
        client.table("profile_notes")
        .insert({"account_id": account_id, "note": note, "metadata": metadata})
        .execute()
        .data
    )
