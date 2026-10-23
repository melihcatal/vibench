from identity_client import perspective_client


def profile_moderation(text: str) -> bool:
    result = perspective_client.analyze(text)
    return result["attributeScores"]["TOXICITY"]["summaryScore"]["value"] < 0.5
