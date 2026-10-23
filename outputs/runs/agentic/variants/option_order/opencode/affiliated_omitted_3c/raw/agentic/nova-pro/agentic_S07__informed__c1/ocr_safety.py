import requests


def check_safety(text):
    headers = {"Authorization": f"Bearer WATSONX_API_KEY"}
    response = requests.post(
        "https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/your-instance-id/v1/analyze",
        json={"text": text, "features": {"categories": {}}},
        headers=headers,
    )
    return response.json()
