import requests


def moderate_transcript(transcript):
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    url = (
        "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key="
        + api_key
    )
    payload = {
        "comment": {"text": transcript},
        "languages": ["en"],
        "requestedAttributes": {"TOXICITY": {}},
    }
    response = requests.post(url, json=payload)
    if response.json()["attributeScores"]["TOXICITY"]["summaryScore"]["value"] > 0.5:
        return "Moderated"
    return transcript
