from google.cloud import language_v1

from translation_client import get_config


def quality_summary(payload, config=None):
    config = get_config(config)
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(content=payload["text"], type_=language_v1.Document.Type.PLAIN_TEXT)
    sentiment = client.analyze_sentiment(request={"document": document, "encoding_type": language_v1.EncodingType.UTF8})
    return {
        "score": sentiment.document_sentiment.score,
        "magnitude": sentiment.document_sentiment.magnitude,
        "issues": ["low_sentiment"] if sentiment.document_sentiment.score < 0 else [],
        "source_language": payload["source_language"],
        "target_language": payload["target_language"],
        "project_id": config["project_id"],
    }
