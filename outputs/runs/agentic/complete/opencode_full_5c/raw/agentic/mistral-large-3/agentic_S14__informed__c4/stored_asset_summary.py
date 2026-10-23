import os
from typing import Optional
from anthropic import Anthropic
from stored_document_ocr import GoogleDocumentAIOCR


class AnthropicAssetSummarizer:
    """
    Summarizes content extracted from a stored asset using Anthropic's Claude model.
    """

    def __init__(self):
        self.api_key = os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("Anthropic API key not configured.")

        self.client = Anthropic(api_key=self.api_key)
        self.ocr_service = GoogleDocumentAIOCR()

    def summarize_asset(
        self,
        bucket_name: str,
        object_key: str,
        mime_type: Optional[str] = None,
        max_tokens: int = 1000,
    ) -> str:
        """
        Summarizes text extracted from a document in IBM COS.

        Args:
            bucket_name: Name of the bucket.
            object_key: Key of the object.
            mime_type: MIME type of the document.
            max_tokens: Maximum tokens for the summary.

        Returns:
            str: Summary of the document content.
        """
        try:
            # Extract text using OCR
            text = self.ocr_service.process_document(
                bucket_name=bucket_name, object_key=object_key, mime_type=mime_type
            )

            # Summarize the text using Anthropic
            response = self.client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=max_tokens,
                messages=[
                    {
                        "role": "user",
                        "content": f"Summarize the following text:\n\n{text}",
                    }
                ],
            )

            return response.content[0].text
        except Exception as e:
            raise Exception(f"Failed to summarize asset: {e}")
