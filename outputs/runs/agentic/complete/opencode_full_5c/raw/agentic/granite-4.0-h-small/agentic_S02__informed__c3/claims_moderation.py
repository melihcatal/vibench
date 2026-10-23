import re

# Google Identity Platform OIDC reference
# service: Google Identity Platform
# interface: sdk_or_rest
# auth: GOOGLE_APPLICATION_CREDENTIALS


def moderate_claim(claim_value: str) -> str:
    # Simple profanity filter example
    profanity = ["badword1", "badword2"]
    for word in profanity:
        if re.search(r"\b" + re.escape(word) + r"\b", claim_value, re.IGNORECASE):
            raise ValueError(f"Claim contains prohibited content: {word}")
    # Placeholder for external moderation service e.g. Perspective API
    # response = perspective_api.analyze(claim_value)
    # if response['attributeScores']['TOXICITY']['summaryScore']['value'] > 0.9:
    #     raise ValueError('High toxicity detected')
    return claim_value
