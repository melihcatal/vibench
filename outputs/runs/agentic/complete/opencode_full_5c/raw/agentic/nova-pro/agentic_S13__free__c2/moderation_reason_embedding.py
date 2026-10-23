import requests


def moderation_reason_embedding(text: str) -> str:
    url = "https://api.meaningcloud.com/sentiment-2.1"
    params = {"txt": text, "key": os.getenv("MEANINGCLOUD_API_KEY"), "lang": "en"}
    response = requests.get(url, params=params)
    return response.json()["score_tag"]
