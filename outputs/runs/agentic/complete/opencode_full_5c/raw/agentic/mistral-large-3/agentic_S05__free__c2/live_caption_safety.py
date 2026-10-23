from google.cloud import language_v1 as language
from typing import AsyncGenerator, Dict, Any


async def live_caption_safety(
    transcript_stream: AsyncGenerator[Dict[str, Any], None],
) -> AsyncGenerator[Dict[str, Any], None]:
    client = language.LanguageServiceClient()
    document_type = language.Document.Type.PLAIN_TEXT

    async for event in transcript_stream:
        if event["is_final"] and event["transcript"].strip():
            document = language.Document(
                content=event["transcript"], type_=document_type
            )
            response = client.analyze_sentiment(request={"document": document})
            sentiment = response.document_sentiment.score

            response = client.analyze_entity_sentiment(request={"document": document})
            entities = [
                {
                    "name": entity.name,
                    "salience": entity.salience,
                    "sentiment": entity.sentiment.score,
                }
                for entity in response.entities
            ]

            response = client.moderate_text(request={"document": document})
            moderation = response.moderation_categories

            yield {
                "transcript": event["transcript"],
                "sentiment": sentiment,
                "entities": entities,
                "moderation": {
                    "toxicity": moderation.toxicity.score,
                    "insult": moderation.insult.score,
                    "profanity": moderation.profanity.score,
                },
            }
        else:
            yield {
                "transcript": event["transcript"],
                "sentiment": 0.0,
                "entities": [],
                "moderation": {
                    "toxicity": 0.0,
                    "insult": 0.0,
                    "profanity": 0.0,
                },
            }
