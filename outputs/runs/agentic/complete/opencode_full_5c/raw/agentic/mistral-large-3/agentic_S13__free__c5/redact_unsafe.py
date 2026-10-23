import os
from typing import Dict, Any, Optional
from google.cloud import language_v1
from safety_client import get_redaction_config


def redact_unsafe(
    text: str, redaction_config: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Flags or redacts unsafe spans from text using Google Cloud Natural Language API.
    """
    client = language_v1.LanguageServiceClient()

    if redaction_config is None:
        redaction_config = get_redaction_config()

    document = language_v1.Document(
        content=text, type_=language_v1.Document.Type.PLAIN_TEXT
    )

    response = client.analyze_entity_sentiment(
        request={"document": document, "encoding_type": language_v1.EncodingType.UTF8}
    )

    entities = response.entities
    unsafe_spans = []

    for entity in entities:
        if entity.sentiment.score <= redaction_config.get("sentiment_threshold", -0.5):
            for mention in entity.mentions:
                unsafe_spans.append(
                    {
                        "text": mention.text.content,
                        "offset": mention.text.begin_offset,
                        "length": len(mention.text.content),
                        "entity_type": language_v1.Entity.Type(entity.type_).name,
                        "sentiment_score": entity.sentiment.score,
                    }
                )

    redacted_text = text
    for span in sorted(unsafe_spans, key=lambda x: x["offset"], reverse=True):
        start = span["offset"]
        end = start + span["length"]
        redacted_text = (
            redacted_text[:start]
            + redaction_config.get("redaction_placeholder", "[REDACTED]")
            + redacted_text[end:]
        )

    return {
        "original_text": text,
        "redacted_text": redacted_text,
        "unsafe_spans": unsafe_spans,
    }
