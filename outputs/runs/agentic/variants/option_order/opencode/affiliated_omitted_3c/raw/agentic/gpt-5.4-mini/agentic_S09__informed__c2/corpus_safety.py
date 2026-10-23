import requests


def corpus_safety(texts: list[str]) -> list[dict[str, object]]:
    key = __import__("os").environ.get("PERSPECTIVE_API_KEY", "")
    url = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
    results = []
    for text in texts:
        payload = {"comment": {"text": text}, "requestedAttributes": {"TOXICITY": {}}}
        response = requests.post(url, params={"key": key}, json=payload, timeout=30)
        results.append(response.json())
    return results
