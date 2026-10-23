import requests

TISANE_API_KEY = os.getenv("TISANE_API_KEY")


def check_platform_output_safety(output: str) -> Dict[str, Any]:
    headers = {"Authorization": f"Bearer {TISANE_API_KEY}"}
    response = requests.post(
        "https://api.tisane.com/v1/moderation", headers=headers, json={"text": output}
    )
    return response.json()
