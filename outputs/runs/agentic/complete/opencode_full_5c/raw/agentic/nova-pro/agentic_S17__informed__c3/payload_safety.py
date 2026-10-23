import requests


def payload_safety(decrypted_text):
    perspective_api_key = "YOUR_PERSPECTIVE_API_KEY"
    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={perspective_api_key}"
    data = {
        "comment": {"text": decrypted_text},
        "requestedAttributes": {"TOXICITY": {}},
    }
    response = requests.post(url, json=data)
    return response.json()
