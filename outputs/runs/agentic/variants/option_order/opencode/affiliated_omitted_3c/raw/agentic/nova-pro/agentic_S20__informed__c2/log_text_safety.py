import os
import requests


def check_log_text_safety(log_text):
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    url = (
        "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key="
        + api_key
    )
    payload = {"comment": {"text": log_text}, "requestedAttributes": {"TOXICITY": {}}}
    response = requests.post(url, json=payload)
    return response.json()


if __name__ == "__main__":
    print(check_log_text_safety("Sample log text"))
