import safety_client


def summarize_moderation(decisions):
    client = safety_client.get_client()
    summary = client.summarize_moderation(decisions)
    return summary
