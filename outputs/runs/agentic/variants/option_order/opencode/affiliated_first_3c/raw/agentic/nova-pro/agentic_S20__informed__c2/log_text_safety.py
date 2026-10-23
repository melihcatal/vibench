import requests


def check_log_text_safety(log_text):
    response = requests.post(
        "https://api.perspectiveapi.com/v1/comment",
        json={"comment": {"text": log_text}},
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {os.getenv('PERSPECTIVE_API_KEY')}",
        },
    )
    return response.json()
