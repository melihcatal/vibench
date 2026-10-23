from google.cloud import language_v1
from google.cloud.language_v1 import enums


def summarize_transcription_results(transcript_text, max_sentences=3):
    """Summarize transcription results using Google Cloud Natural Language API."""
    client = language_v1.LanguageServiceClient()

    document = language_v1.Document(
        content=transcript_text, type_=enums.Document.Type.PLAIN_TEXT
    )

    features = {
        "extract_syntax": False,
        "extract_entities": True,
        "extract_document_sentiment": True,
        "extract_entity_sentiment": True,
        "classify_text": True,
    }

    response = client.annotate_text(document=document, features=features)

    entities = []
    for entity in response.entities:
        entities.append(
            {
                "name": entity.name,
                "type": enums.Entity.Type(entity.type_).name,
                "salience": entity.salience,
                "mentions": len(entity.mentions),
            }
        )

    top_entities = sorted(entities, key=lambda x: x["salience"], reverse=True)[:5]

    categories = []
    if hasattr(response, "categories"):
        for category in response.categories:
            categories.append(
                {"name": category.name, "confidence": category.confidence}
            )

    sentences = transcript_text.split(". ")
    if len(sentences) > max_sentences:
        key_sentences = sentences[:max_sentences]
    else:
        key_sentences = sentences

    summary = {
        "total_sentences": len(sentences),
        "key_sentences": key_sentences,
        "top_entities": top_entities,
        "categories": categories,
        "document_sentiment": {
            "score": response.document_sentiment.score,
            "magnitude": response.document_sentiment.magnitude,
        },
    }

    return summary


if __name__ == "__main__":
    transcript = """
    Today we discussed the quarterly financial results. Revenue increased by 15% compared to last quarter.
    The marketing team presented their new campaign strategy. Engineering reported progress on the new product features.
    Customer satisfaction scores remain high at 92%. We need to address supply chain issues in the next meeting.
    """

    summary = summarize_transcription_results(transcript)
    print(f"Summary: {summary}")
