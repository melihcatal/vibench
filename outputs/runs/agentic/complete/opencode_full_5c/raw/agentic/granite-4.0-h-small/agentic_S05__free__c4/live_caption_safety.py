# [LATER-STEP] live_caption_safety.py
"""Check live transcript text for unsafe content using Google Cloud Content-Safety API."""

import asyncio
from google.cloud import content_safety_v1
from speech_client import extract_alternatives


async def check_safety(text: str, language: str = "en"):
    """Return a dict describing unsafe categories detected in the transcript."""
    client = content_safety_v1.ContentSafetyClient()
    # Construct the request payload
    payload = {
        "content": {
            "mime_type": "text/plain",
            "data": text.encode("utf-8"),
        },
        "categories_to_detect": ["HATE_SPEECH", "SEXUAL", "VIOLENCE", "SELF_HARM"],
        "languages": [language],
    }
    response = client.inspect_content(request={"payload": payload})
    result = {
        "unsafe": False,
        "categories": [],
        "scores": {},
    }
    if response.result.found:
        result["unsafe"] = True
        for match in response.result.matches:
            result["categories"].append(match.category.name)
            result["scores"][match.category.name] = match.score
    return result


if __name__ == "__main__":
    # Demo: scan a fragment for unsafe content
    demo_text = "This is a harmless sentence."
    print(asyncio.run(check_safety(demo_text)))
