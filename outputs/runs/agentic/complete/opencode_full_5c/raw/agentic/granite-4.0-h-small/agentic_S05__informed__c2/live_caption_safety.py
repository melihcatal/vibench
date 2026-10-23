import requests, json

PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def check_unsafe_content(text):
    """Check live transcript text for unsafe content using Perspective API."""
    key = "PERSPECTIVE_API_KEY"
    headers = {"content-type": "application/json"}
    payload = {
        "comment": {"text": text},
        "languages": ["en"],
        "requestedAttributes": {"TOXICITY": {}},
    }
    r = requests.post(PERSPECTIVE_API_URL, headers=headers, json=payload)
    r.raise_for_status()
    score = r.json()["attributeScores"]["TOXICITY"]["summaryScore"]["value"]
    return score > 0.8  # threshold for unsafe (customize as needed)


# Example usage: print(check_unsafe_content('Some hateful remark here.'))
