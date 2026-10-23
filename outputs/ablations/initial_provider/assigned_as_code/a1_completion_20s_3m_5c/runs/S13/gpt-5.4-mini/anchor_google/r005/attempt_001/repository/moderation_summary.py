import requests


def moderation_summary(payload, config=None):
    config = config or {}
    response = requests.post(
        "https://api.openai.com/v1/responses",
        headers={"Authorization": f"Bearer {config.get('api_key')}", "Content-Type": "application/json"},
        json={
            "model": config.get("model") or "gpt-5.4-mini",
            "input": payload.get("decisions", []),
        },
        timeout=30,
    )
    response.raise_for_status()
    return {"summary": response.json()}
