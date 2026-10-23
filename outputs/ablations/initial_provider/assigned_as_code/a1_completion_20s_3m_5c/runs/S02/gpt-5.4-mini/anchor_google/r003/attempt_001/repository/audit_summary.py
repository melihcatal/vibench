import requests


def audit_summary(payload, config=None):
    events = payload.get("events", [])
    response = requests.post(
        "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent",
        params={"key": (config or {}).get("api_key")},
        json={"contents": [{"parts": [{"text": "Summarize federated-login audit events: " + str(events)}]}]},
        timeout=30,
    )
    response.raise_for_status()
    data = response.json()
    text = data["candidates"][0]["content"]["parts"][0]["text"]
    return {"summary": text}
