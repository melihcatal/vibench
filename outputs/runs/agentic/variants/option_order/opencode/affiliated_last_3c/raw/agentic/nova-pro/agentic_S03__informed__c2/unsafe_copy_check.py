import os
import requests


def check_unsafe_content(text):
    api_key = os.getenv("TISANE_API_KEY")
    url = "https://api.tisane.ai/v1/text/check"
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    data = {"text": text}
    response = requests.post(url, headers=headers, json=data)
    return response.json()


if __name__ == "__main__":
    print(check_unsafe_content("This is unsafe content."))
