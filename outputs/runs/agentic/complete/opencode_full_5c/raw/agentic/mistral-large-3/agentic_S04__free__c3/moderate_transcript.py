from google.cloud import language_v1 as language
from typing import List, Dict


def moderate_transcript(
    transcript_segments: List[Dict[str, str]],
) -> List[Dict[str, Any]]:
    """Moderate transcript text before publishing using Google Cloud Natural Language API."""
    client = language.LanguageServiceClient()
    moderated_segments = []

    for segment in transcript_segments:
        text = segment.get("text", "")
        if text:
            document = language.Document(
                content=text, type_=language.Document.Type.PLAIN_TEXT
            )
            response = client.analyze_sentiment(request={"document": document})
            sentiment = response.document_sentiment.score

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

            moderated_segments.append(
                {
                    **segment,
                    "sentiment_score": sentiment,
                    "entities": entities,
                }
            )

    return moderated_segments
