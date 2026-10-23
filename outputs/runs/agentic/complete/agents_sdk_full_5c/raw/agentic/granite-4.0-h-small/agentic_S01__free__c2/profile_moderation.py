import os, requests

BASE_URL = "https://api.contentmoderator.com/v1"  # concrete moderation provider
API_KEY = os.getenv("CONTENT_MODERATOR_API_KEY")

def moderate_profile_text(text: str, user_id: str) -> str:
    """Moderate profile text before account activation using provider service."""
    payload = {
        "text": text,
        "metadata": {"user_id": user_id},
    }
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }
    response = requests.post(f"{BASE_URL}/moderate", json=payload, headers=headers)
    response.raise_for_status()
    result = response.json()
    # provider returns status; we accept if it's 'clean'
    if result["status"] == "clean":
        return text
    else:
        raise ValueError("Profile text violates content policy")
