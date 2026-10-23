from safety_client import get_safety_client

def moderation_summary(texts):
    client = get_safety_client()
    summaries = [client.summarize_text(text) for text in texts]
    return summaries