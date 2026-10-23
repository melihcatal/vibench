import requests


def profile_moderation(text: str):
    endpoint = __import__("os").environ["AZURE_CONTENT_SAFETY_ENDPOINT"].rstrip("/")
    key = __import__("os").environ["AZURE_CONTENT_SAFETY_KEY"]
    url = f"{endpoint}/contentsafety/text:analyze?api-version=2023-10-01"
    headers = {"Ocp-Apim-Subscription-Key": key, "Content-Type": "application/json"}
    payload = {"text": text, "categories": ["Hate", "SelfHarm", "Sexual", "Violence"]}
    resp = requests.post(url, headers=headers, json=payload, timeout=30)
    resp.raise_for_status()
    return resp.json()
