import requests

# Initialize the client
api_key = os.getenv("PERSPECTIVE_API_KEY")


def check_safety(text):
    response = requests.post(
        "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze",
        json={
            "comment": {"text": text},
            "languages": ["en"],
            "requestedAttributes": {"TOXICITY": {}},
        },
        headers={"Authorization": f"Bearer {api_key}"},
    )
    return response.json()
