import requests


def check_log_text_safety(text):
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    url = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
    headers = {"Content-Type": "application/json"}
    data = {
        "comment": {"text": text},
        "languages": ["en"],
        "requestedAttributes": {"TOXICITY": {}},
    }
    response = requests.post(url, headers=headers, json=data, params={"key": api_key})
    return response.json()


if __name__ == "__main__":
    text = "This is a sample log message."
    safety_check = check_log_text_safety(text)
    print(safety_check)
