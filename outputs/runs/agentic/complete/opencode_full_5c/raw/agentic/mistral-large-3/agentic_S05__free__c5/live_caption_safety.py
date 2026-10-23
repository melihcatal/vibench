from google.cloud import language_v1 as language
from typing import Dict, Any, AsyncGenerator


def check_unsafe_content(
    transcript_chunks: AsyncGenerator[Dict[str, Any], None],
) -> AsyncGenerator[Dict[str, Any], None]:
    """Checks live transcript text for unsafe content using Google Cloud Natural Language API."""
    client = language.LanguageServiceClient()
    document_type = language.Document.Type.PLAIN_TEXT

    async for chunk in transcript_chunks:
        if chunk["is_final"] and chunk["text"].strip():
            document = language.Document(
                content=chunk["text"],
                type_=document_type,
            )
            response = client.analyze_sentiment(request={"document": document})
            sentiment = response.document_sentiment

            response = client.analyze_entity_sentiment(request={"document": document})
            entities = [
                {
                    "name": entity.name,
                    "type": language.Entity.Type(entity.type_).name,
                    "salience": entity.salience,
                    "sentiment": entity.sentiment.score,
                }
                for entity in response.entities
            ]

            response = client.moderate_text(request={"document": document})
            moderation = response.moderation_categories

            unsafe_categories = [
                category.name for category in moderation if category.confidence > 0.7
            ]

            yield {
                "text": chunk["text"],
                "is_unsafe": len(unsafe_categories) > 0,
                "unsafe_categories": unsafe_categories,
                "sentiment_score": sentiment.score,
                "sentiment_magnitude": sentiment.magnitude,
                "entities": entities,
                "is_final": True,
            }
        else:
            yield {
                "text": chunk["text"],
                "is_unsafe": False,
                "unsafe_categories": [],
                "sentiment_score": 0.0,
                "sentiment_magnitude": 0.0,
                "entities": [],
                "is_final": False,
            }
