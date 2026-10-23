from google.cloud import language_v1 as language
from typing import AsyncIterable


class LiveCaptionSafetyChecker:
    """Checks live transcript text for unsafe content."""

    def __init__(self):
        self.client = language.LanguageServiceClient()
        self._unsafe_categories = {
            "TOXICITY",
            "SEVERE_TOXICITY",
            "IDENTITY_ATTACK",
            "INSULT",
            "PROFANITY",
            "THREAT",
        }

    async def check_stream(
        self, transcript_stream: AsyncIterable[str]
    ) -> AsyncIterable[Dict[str, Any]]:
        """Checks a stream of transcripts for unsafe content."""
        async for transcript in transcript_stream:
            document = language.Document(
                content=transcript, type_=language.Document.Type.PLAIN_TEXT
            )
            response = self.client.analyze_sentiment(
                request={
                    "document": document,
                    "features": {"extract_document_sentiment": True},
                }
            )
            sentiment = response.document_sentiment.score

            response = self.client.analyze_entity_sentiment(
                request={"document": document}
            )
            entities = [
                {"name": entity.name, "sentiment": entity.sentiment.score}
                for entity in response.entities
            ]

            response = self.client.moderate_text(request={"document": document})
            moderation = response.moderation_categories

            unsafe_content = any(
                category.confidence > 0.7
                for category in moderation
                if category.name in self._unsafe_categories
            )

            yield {
                "transcript": transcript,
                "is_unsafe": unsafe_content,
                "sentiment": sentiment,
                "entities": entities,
            }
