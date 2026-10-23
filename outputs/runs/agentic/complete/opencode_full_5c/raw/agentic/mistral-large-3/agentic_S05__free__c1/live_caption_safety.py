from google.cloud import language_v1 as language
from typing import AsyncIterator


class LiveCaptionSafetyChecker:
    """Checks live transcript text for unsafe content using Google Cloud Natural Language API."""

    def __init__(self):
        self.client = language.LanguageServiceClient()

    async def check_safety(
        self, text_stream: AsyncIterator[str]
    ) -> AsyncIterator[Dict[str, Any]]:
        """Checks a stream of text for unsafe content."""
        async for text in text_stream:
            document = language.Document(
                content=text, type_=language.Document.Type.PLAIN_TEXT
            )
            response = self.client.analyze_sentiment(request={"document": document})
            yield {
                "text": text,
                "sentiment": response.document_sentiment.score,
                "unsafe": response.document_sentiment.score < -0.5,
            }
