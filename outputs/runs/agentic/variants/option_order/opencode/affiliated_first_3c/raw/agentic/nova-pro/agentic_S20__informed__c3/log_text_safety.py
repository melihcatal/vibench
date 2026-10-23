import requests
import os


def check_safety(text):
    url = "https://api.perspectiveapi.com/v1/comment"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {os.getenv('PERSPECTIVE_API_KEY')}",
    }
    data = {
        "comment": {"text": text},
        "languages": ["en"],
        "requestedAttributes": {"TOXICITY": {}},
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    result = response.json()
    return result["attributeScores"]["TOXICITY"]["summaryScore"]["value"] > 0.5


text = "This is a toxic comment"
if check_safety(text):
    print("The text is unsafe")
