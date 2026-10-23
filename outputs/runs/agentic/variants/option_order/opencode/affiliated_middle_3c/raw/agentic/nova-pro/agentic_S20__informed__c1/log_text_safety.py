import requests


def check_log_text_safety(log_text):
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    url = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
    headers = {"Content-Type": "application/json"}
    payload = {
        "comment": {"text": log_text},
        "languages": ["en"],
        "requestedAttributes": {"TOXICITY": {}},
    }
    response = requests.post(
        url, headers=headers, params={"key": api_key}, json=payload
    )
    return response.json()


if __name__ == "__main__":
    print(check_log_text_safety("This is a test log message."))
