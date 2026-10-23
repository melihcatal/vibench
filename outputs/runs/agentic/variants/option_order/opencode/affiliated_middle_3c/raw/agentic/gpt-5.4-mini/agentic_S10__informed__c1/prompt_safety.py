import requests


PERSPECTIVE_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def check_prompt(prompt: str):
    params = {"key": __import__("os").getenv("PERSPECTIVE_API_KEY", "")}
    data = {"comment": {"text": prompt}, "requestedAttributes": {"TOXICITY": {}}}
    return requests.post(PERSPECTIVE_URL, params=params, json=data, timeout=30).json()


def check_generated_text(text: str):
    return check_prompt(text)
