import requests


def summarize_audit_events(text: str) -> str:
    response = requests.post(
        "https://api.openai.com/v1/responses",
        headers={"Authorization": f"Bearer {__import__('os').environ.get('OPENAI_API_KEY', '')}"},
        json={"model": "gpt-5.4-mini", "input": f"Summarize federated-login audit events:\n{text}"},
        timeout=60,
    )
    response.raise_for_status()
    data = response.json()
    return data.get("output_text", "")
