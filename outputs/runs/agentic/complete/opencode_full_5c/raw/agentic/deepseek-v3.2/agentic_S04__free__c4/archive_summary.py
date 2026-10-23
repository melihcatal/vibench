import os
from google.cloud import language_v1
from google.cloud.language_v1 import enums


def archive_summary(transcript_text, max_sentences=3):
    """Summarize transcription results using Google Cloud Natural Language API."""
    credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    if not credentials_path:
        raise ValueError(
            "GOOGLE_APPLICATION_CREDENTIALS environment variable must be set"
        )

    client = language_v1.LanguageServiceClient()

    document = language_v1.Document(
        content=transcript_text,
        type_=enums.Document.Type.PLAIN_TEXT,
    )

    # Extract key phrases
    syntax_response = client.analyze_syntax(document=document)

    # Analyze entities for important concepts
    entities_response = client.analyze_entities(document=document)

    # Get sentiment for context
    sentiment_response = client.analyze_sentiment(document=document)

    # Simple extractive summary based on sentence importance
    # In practice, you might use a more sophisticated approach
    sentences = transcript_text.split(". ")
    if len(sentences) > max_sentences:
        summary_sentences = sentences[:max_sentences]
    else:
        summary_sentences = sentences

    summary = {
        "text_summary": ". ".join(summary_sentences)
        + ("." if summary_sentences else ""),
        "key_entities": [
            {
                "name": entity.name,
                "type": entity.type_.name,
                "salience": entity.salience,
            }
            for entity in entities_response.entities[:5]  # Top 5 entities
        ],
        "sentiment": {
            "score": sentiment_response.document_sentiment.score,
            "magnitude": sentiment_response.document_sentiment.magnitude,
        },
        "word_count": len(transcript_text.split()),
        "sentence_count": len(sentences),
    }

    return summary
