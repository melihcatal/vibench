import json

from identity_client import comprehend_client, normalize_profile_text


def profile_moderation(text: str):
    client = comprehend_client()
    payload = normalize_profile_text(text)
    return client.detect_toxic_content(TextSegments=[{"Text": payload, "Index": 0}])
