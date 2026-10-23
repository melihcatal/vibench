import requests


# Moderate free-text claims or notes
def moderate_claims(claims):
    headers = {"Authorization": f"Bearer {os.environ['PERSPECTIVE_API_KEY']}"}
    response = requests.post(
        "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={os.environ['PERSPECTIVE_API_KEY']}",
        json={"comment": {"text": claims}, "requestedAttributes": {"TOXICITY": {}}},
        headers=headers,
    )
    response.raise_for_status()
    return response.json()
