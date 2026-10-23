from google.cloud import language_v1 as language
from typing import Dict, List


def archive_summary(transcript_text: str) -> Dict[str, Any]:
    """Summarize transcription results using Google Cloud Natural Language API."""
    client = language.LanguageServiceClient()
    document = language.Document(
        content=transcript_text, type_=language.Document.Type.PLAIN_TEXT
    )

    response = client.analyze_entities(request={"document": document})
    entities = [
        {
            "name": entity.name,
            "type": language.Entity.Type(entity.type_).name,
            "salience": entity.salience,
        }
        for entity in response.entities
    ]

    response = client.analyze_sentiment(request={"document": document})
    sentiment = response.document_sentiment

    response = client.classify_text(request={"document": document})
    categories = [category.name for category in response.categories]

    return {
        "summary": {
            "key_entities": entities,
            "sentiment": {"score": sentiment.score, "magnitude": sentiment.magnitude},
            "categories": categories,
        }
    }
