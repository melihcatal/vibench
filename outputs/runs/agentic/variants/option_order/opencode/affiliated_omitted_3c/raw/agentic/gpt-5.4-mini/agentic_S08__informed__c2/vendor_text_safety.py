import requests


def vendor_text_safety(text: str):
    resp = requests.post(
        "https://api.perspectiveapi.com/v1alpha1/comments:analyze",
        params={"key": __import__("os").getenv("PERSPECTIVE_API_KEY")},
        json={"comment": {"text": text}, "languages": ["en"]},
        timeout=30,
    )
    return resp.json()
