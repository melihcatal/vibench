import requests


def secret_label_safety(label: str, notes: str):
    api_key = __import__("os").getenv("PERSPECTIVE_API_KEY", "")
    payload = {
        "comment": {"text": f"{label}\n{notes}"},
        "requestedAttributes": {"TOXICITY": {}},
    }
    r = requests.post(
        f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}",
        json=payload,
        timeout=30,
    )
    r.raise_for_status()
    return r.json()
