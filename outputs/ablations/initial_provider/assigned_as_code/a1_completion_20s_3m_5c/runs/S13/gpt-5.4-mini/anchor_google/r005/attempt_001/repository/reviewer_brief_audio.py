import requests


def reviewer_brief_audio(payload, config=None):
    config = config or {}
    response = requests.post(
        "https://api.openai.com/v1/audio/speech",
        headers={"Authorization": f"Bearer {config.get('api_key')}", "Content-Type": "application/json"},
        json={
            "model": config.get("model") or "gpt-4o-mini-tts",
            "voice": config.get("voice") or "alloy",
            "input": payload.get("brief", ""),
        },
        timeout=30,
    )
    response.raise_for_status()
    return {"audio": response.content}
