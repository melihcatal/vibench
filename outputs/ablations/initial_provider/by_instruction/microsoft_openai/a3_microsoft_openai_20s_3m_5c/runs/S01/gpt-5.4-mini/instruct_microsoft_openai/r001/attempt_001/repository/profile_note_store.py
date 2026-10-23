import os

import requests


def profile_note_store(note: str, metadata: dict):
    token = os.environ["SUPABASE_SERVICE_ROLE_KEY"]
    url = os.environ["SUPABASE_URL"].rstrip("/") + "/rest/v1/profile_notes"
    response = requests.post(
        url,
        headers={
            "apikey": token,
            "authorization": f"Bearer {token}",
            "content-type": "application/json",
            "prefer": "return=representation",
        },
        json={"note": note, "metadata": metadata},
        timeout=30,
    )
    response.raise_for_status()
    return response.json()
