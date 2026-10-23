from typing import Optional

from google.cloud import language_v1
from google.api_core.exceptions import GoogleAPIError


def stored_asset_summary(text: str, language: Optional[str] = None) -> str:
    """
    Summarizes content extracted from a stored asset using Google Cloud Natural Language API.

    Args:
        text: Text to summarize.
        language: Optional language code of the text (e.g., 'en', 'es').

    Returns:
        A summary of the text.

    Raises:
        GoogleAPIError: If the summarization fails.
    """
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(
        content=text, type_=language_v1.Document.Type.PLAIN_TEXT, language=language
    )

    response = client.analyze_entities(request={"document": document})
    entities = [entity.name for entity in response.entities]

    # Simple summarization by extracting key entities
    return f"Summary: This document mentions {', '.join(entities)}."
