import requests


def check_corpus_text(text):
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    url = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
    payload = {"comment": {"text": text}, "requestedAttributes": {"TOXICITY": {}}}
    response = requests.post(f"{url}?key={api_key}", json=payload, timeout=30)
    response.raise_for_status()
    return response.json()
