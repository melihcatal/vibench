import requests


def unsafe_copy_check(text):
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    headers = {"Authorization": f"Bearer {api_key}"}
    response = requests.post(
        "https://api.perspectiveapi.com/v1alpha1/commentanalyzer",
        headers=headers,
        json={"comment": {"text": text}},
    )
    return response.json()
