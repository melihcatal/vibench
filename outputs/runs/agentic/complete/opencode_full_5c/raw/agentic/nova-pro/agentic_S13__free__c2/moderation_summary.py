from safety_models import SafetyResponse


def moderation_summary(responses: List[SafetyResponse]) -> str:
    summary = "Moderation Summary:\n"
    for i, response in enumerate(responses):
        summary += f"Message {i + 1}: {response.labels}\n"
    return summary
