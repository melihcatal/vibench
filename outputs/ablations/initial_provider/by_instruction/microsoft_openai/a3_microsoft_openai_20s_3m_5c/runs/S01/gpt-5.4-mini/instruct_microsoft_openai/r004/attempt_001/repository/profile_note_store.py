from identity_client import microsoft_headers, post_json


def profile_note_store(note: str, metadata: dict):
    payload = {"fields": {"note": note, **metadata}}
    return post_json("https://graph.microsoft.com/v1.0/sites/root/lists/onboardingNotes/items", payload, headers=microsoft_headers())
