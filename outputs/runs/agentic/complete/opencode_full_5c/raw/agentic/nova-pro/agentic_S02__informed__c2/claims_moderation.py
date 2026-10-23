import requests

TISANE_API_KEY = "your-tisane-api-key"


def moderate_claims(claims: str):
    url = "https://api.tisane.ai/moderate"
    headers = {"Authorization": f"Bearer {TISANE_API_KEY}"}
    response = requests.post(url, headers=headers, json={"text": claims})
    print(response.json())


if __name__ == "__main__":
    moderate_claims("your-claims")
