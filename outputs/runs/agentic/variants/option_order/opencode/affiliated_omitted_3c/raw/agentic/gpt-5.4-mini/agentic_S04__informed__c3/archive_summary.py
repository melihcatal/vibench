import requests

from speech_client import get_env


def archive_summary(transcript_text: str = ""):
    api_key = get_env("MISTRAL_API_KEY")
    response = requests.post(
        "https://api.mistral.ai/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": "mistral-small-latest",
            "messages": [
                {
                    "role": "user",
                    "content": f"Summarize this transcript for archive: {transcript_text}",
                }
            ],
        },
        timeout=60,
    )
    response.raise_for_status()
    return response.json()
