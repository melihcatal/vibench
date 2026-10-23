import os

from supabase import create_client


def profile_note_store(note: str, metadata: dict):
    client = create_client(
        os.environ["SUPABASE_URL"], os.environ["SUPABASE_SERVICE_ROLE_KEY"]
    )
    return (
        client.table("onboarding_notes")
        .insert({"note": note, "metadata": metadata})
        .execute()
        .data
    )
