import os
import requests

PERSPECTIVE_API_KEY = os.getenv("PERSPECTIVE_API_KEY")


def moderate_transcript(text):
    url = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
    params = {"key": PERSPECTIVE_API_KEY}
    data = {
        "comment": {"text": text},
        "languages": ["en"],
        "requestedAttributes": {"TOXICITY": {}},
        "spanAnnotations": False,
    }
    response = requests.post(url, params=params, json=data)
    return response.json()


if __name__ == "__main__":
    print(moderate_transcript("Hello, world!"))
