import requests


def payload_safety(decrypted_text):
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    url = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
    headers = {"Content-Type": "application/json"}
    data = {
        "comment": {"text": decrypted_text},
        "languages": ["en"],
        "requestedAttributes": {"TOXICITY": {}},
    }
    response = requests.post(url, json=data, headers=headers)
    return response.json()
