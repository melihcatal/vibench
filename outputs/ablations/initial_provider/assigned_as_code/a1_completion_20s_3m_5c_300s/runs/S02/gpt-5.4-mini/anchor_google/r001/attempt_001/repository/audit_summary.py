import requests


def audit_summary(payload, config=None):
    response = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers={"Authorization": f"Bearer {config['api_key']}", "Content-Type": "application/json"},
        json={
            "model": "gpt-5.4-mini",
            "messages": [{"role": "user", "content": payload["events"]}],
            "temperature": 0,
        },
        timeout=30,
    )
    response.raise_for_status()
    return response.json()
