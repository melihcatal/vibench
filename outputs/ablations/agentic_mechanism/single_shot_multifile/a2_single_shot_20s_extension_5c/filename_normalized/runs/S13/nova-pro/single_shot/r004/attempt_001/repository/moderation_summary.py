from safety_client import get_safety_client

def moderation_summary(texts):
    client = get_safety_client()
    summaries = []
    for text in texts:
        response = client.moderate(text)
        summary = {category: score for category, score in response['categories'].items() if score > 0.5}
        summaries.append(summary)
    return summaries