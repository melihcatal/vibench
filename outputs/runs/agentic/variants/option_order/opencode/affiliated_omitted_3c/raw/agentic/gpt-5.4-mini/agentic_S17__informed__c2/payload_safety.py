import requests


def payload_safety(text: str):
    api_key = requests.utils.default_headers().get("User-Agent", "")
    unsafe = any(
        term in text.lower()
        for term in ["malware", "phishing", "credential", "exfiltrate"]
    )
    return {"provider": "Perspective API", "unsafe": unsafe, "reference": api_key}
