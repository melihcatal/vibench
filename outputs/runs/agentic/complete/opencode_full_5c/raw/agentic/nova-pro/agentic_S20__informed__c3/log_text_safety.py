import requests


def check_log_text_safety(log_text):
    response = requests.post(
        "https://api.perspectiveapi.com/v1/comment",
        headers={"Authorization": "Bearer YOUR_PERSPECTIVE_API_KEY"},
        json={"comment": {"text": log_text}},
    )
    return response.json()
