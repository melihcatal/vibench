import requests


def audit_summary(payload, config=None):
    response = requests.post("https://api.openai.com/v1/responses", headers={"Authorization": f"Bearer {config['openai_api_key']}", "Content-Type": "application/json"}, json={"model": "gpt-5.4-mini", "input": payload["events"]}, timeout=60)
    response.raise_for_status()
    return response.json()
