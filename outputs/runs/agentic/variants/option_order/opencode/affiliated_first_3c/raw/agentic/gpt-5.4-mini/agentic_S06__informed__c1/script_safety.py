import requests


def check_script_safety(text: str, api_key: str, endpoint: str) -> dict:
    url = (
        endpoint.rstrip("/")
        + "/contentsafety/text:analyze?api-version=2024-02-15-preview"
    )
    headers = {"Ocp-Apim-Subscription-Key": api_key, "Content-Type": "application/json"}
    payload = {"text": text}
    return requests.post(url, headers=headers, json=payload, timeout=30).json()
