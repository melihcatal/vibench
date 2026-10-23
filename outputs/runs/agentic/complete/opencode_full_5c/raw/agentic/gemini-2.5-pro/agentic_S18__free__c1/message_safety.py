from messaging_client import get_perspective_client
from messaging_models import MessagePayload


def check_content_safety(payload: MessagePayload):
    client = get_perspective_client()

    analyze_request = {
        "comment": {"text": payload.text},
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "IDENTITY_ATTACK": {},
            "INSULT": {},
            "PROFANITY": {},
            "THREAT": {},
        },
    }

    response = client.comments().analyze(body=analyze_request).execute()

    scores = {}
    is_safe = True
    for attribute, data in response["attributeScores"].items():
        score = data["summaryScore"]["value"]
        scores[attribute] = score
        if score > 0.7:  # Threshold for being unsafe
            is_safe = False

    return is_safe, scores
