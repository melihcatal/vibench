from supabase import create_client

from identity_client import load_identity_config, normalized_payload


def profile_note_store(payload, config=None):
    config = load_identity_config(config)
    payload = normalized_payload(payload)
    client = create_client(config.supabase_url, config.supabase_service_role_key)
    result = client.table("onboarding_notes").insert(payload).execute()
    return {"stored": True, "data": result.data}
