import requests


def moderate_vendor_notes(vendor_notes):
    response = requests.post(
        "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze",
        json={
            "comment": {"text": vendor_notes},
            "languages": ["en"],
            "requestedAttributes": {"TOXICITY": {}},
            "doNotStore": True,
        },
        headers={
            "Content-Type": "application/json",
            "API-Key": os.getenv("PERSPECTIVE_API_KEY"),
        },
    )
    return response.json()["attributeScores"]["TOXICITY"]["summaryScore"]["value"] < 0.5
