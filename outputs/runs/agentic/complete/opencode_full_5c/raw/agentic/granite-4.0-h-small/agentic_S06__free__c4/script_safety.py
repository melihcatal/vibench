# [LATER-STEP] script_safety.py
# Check narration scripts for unsafe content using Google Cloud Content Safeguard API

from google.cloud import content_safeguard


def is_safe(script: str) -> bool:
    """Simple wrapper that returns True if the script passes content safety checks."""
    client = content_safeguard.ContentSafeguardClient()
    # Detect potentially unsafe content (e.g., hate, sexual content, violence)
    response = client.analyze_content({"content": script})
    # Assume the API returns a boolean safe flag (real API would need parsing)
    return response.safe
