from safety_client import get_perspective_client
from safety_models import ModerationAttributes, ModerationDecision


def moderate_text(text: str) -> ModerationDecision:
    client = get_perspective_client()
    analyze_request = {
        "comment": {"text": text},
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
    flagged = False
    for attr, value in response["attributeScores"].items():
        score = value["summaryScore"]["value"]
        scores[attr.lower()] = score
        if score > 0.7:  # Example threshold
            flagged = True

    return ModerationDecision(
        text=text, flagged=flagged, scores=ModerationAttributes.parse_obj(scores)
    )
