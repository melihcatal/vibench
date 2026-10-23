import requests


def check_secret_labels(secret_name):
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"
    headers = {"Content-Type": "application/json"}
    data = {"comment": {"text": secret_name}, "languages": ["en"]}
    response = requests.post(url, headers=headers, json=data)
    return response.json()
