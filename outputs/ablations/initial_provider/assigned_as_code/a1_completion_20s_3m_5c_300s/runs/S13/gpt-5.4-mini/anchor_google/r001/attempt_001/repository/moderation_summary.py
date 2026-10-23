from safety_client import post_perspective


def moderation_summary(payload, config=None):
    text = payload.get("text", "")
    data = post_perspective({"comment": {"text": text}, "languages": ["en"], "requestedAttributes": {"TOXICITY": {}}, "doNotStore": True}, config=config)
    score = data["attributeScores"]["TOXICITY"]["summaryScore"]["value"]
    if score >= 0.8:
        summary = "High-risk content requiring immediate review."
    elif score >= 0.5:
        summary = "Potentially unsafe content for moderator review."
    else:
        summary = "Content appears acceptable."
    return {"summary": summary, "toxicity": score}
