from vision_client import get_perspective_client
from vision_models import ImageLabel


def check_text_safety(labels: list[ImageLabel]) -> dict:
    client = get_perspective_client()

    text_to_check = " ".join([label.description for label in labels])

    if not text_to_check.strip():
        return {}

    analyze_request = {
        "comment": {"text": text_to_check},
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "IDENTITY_ATTACK": {},
            "INSULT": {},
            "PROFANITY": {},
            "THREAT": {},
        },
        "languages": ["en"],
    }

    response = client.comments().analyze(body=analyze_request).execute()

    scores = {}
    if "attributeScores" in response:
        for attribute, data in response["attributeScores"].items():
            scores[attribute] = data["summaryScore"]["value"]

    return scores
