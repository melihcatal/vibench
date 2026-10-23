from google.cloud import language_v2

from observability_client import get_logging_client


def incident_summary(payload, config=None):
    client, cfg = get_logging_client(config)
    messages = payload["messages"]
    text = "\n".join(messages)
    language_client = language_v2.LanguageServiceClient()
    document = language_v2.Document(content=text, type_=language_v2.Document.Type.PLAIN_TEXT)
    sentiment = language_client.analyze_sentiment(request={"document": document}).document_sentiment
    return {"project_id": cfg["project_id"], "summary": {"message_count": len(messages), "score": sentiment.score, "magnitude": sentiment.magnitude}}
