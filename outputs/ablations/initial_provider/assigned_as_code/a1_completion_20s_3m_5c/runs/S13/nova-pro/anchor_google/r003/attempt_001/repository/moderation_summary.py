from safety_client import get_safety_client


def moderation_summary(decisions):
    client = get_safety_client()
    summary = {"total": len(decisions), "unsafe": 0, "safe": 0}
    for decision in decisions:
        if decision["toxicity"] > 0.5:
            summary["unsafe"] += 1
        else:
            summary["safe"] += 1
    return summary