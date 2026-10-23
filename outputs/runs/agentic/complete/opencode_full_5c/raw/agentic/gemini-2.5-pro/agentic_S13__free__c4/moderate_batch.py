from typing import List
from safety_client import get_perspective_client
from safety_models import (
    ModerationAttributes,
    ModerationDecision,
    BatchModerationDecision,
)


def moderate_batch(texts: List[str]) -> BatchModerationDecision:
    client = get_perspective_client()
    decisions = []

    for text in texts:
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
        try:
            response = client.comments().analyze(body=analyze_request).execute()
            scores = {}
            flagged = False
            for attr, value in response["attributeScores"].items():
                score = value["summaryScore"]["value"]
                scores[attr.lower()] = score
                if score > 0.7:
                    flagged = True

            decisions.append(
                ModerationDecision(
                    text=text,
                    flagged=flagged,
                    scores=ModerationAttributes.parse_obj(scores),
                )
            )
        except Exception:
            decisions.append(
                ModerationDecision(
                    text=text, flagged=True, scores=ModerationAttributes()
                )
            )

    return BatchModerationDecision(decisions=decisions)
