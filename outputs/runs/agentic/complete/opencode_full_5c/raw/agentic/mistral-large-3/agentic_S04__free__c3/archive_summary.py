from google.cloud import language_v1 as language
from typing import List, Dict


def archive_summary(transcript_segments: List[Dict[str, str]]) -> str:
    """Summarize transcription results using Google Cloud Natural Language API."""
    client = language.LanguageServiceClient()
    full_text = " ".join([segment.get("text", "") for segment in transcript_segments])

    if not full_text.strip():
        return "No transcript available for summarization."

    document = language.Document(
        content=full_text, type_=language.Document.Type.PLAIN_TEXT
    )
    features = {"extract_document_sentiment": True, "extract_entities": True}
    response = client.annotate_text(
        request={"document": document, "features": features}
    )

    summary = f"Summary of transcript:\n"
    summary += f"- Sentiment: {response.document_sentiment.score:.2f}\n"
    summary += f"- Entities detected: {len(response.entities)}\n"
    summary += f"- Key topics:\n"

    for entity in response.entities[:5]:
        summary += f"  - {entity.name} ({language.Entity.Type(entity.type_).name}): {entity.salience:.2%} salience\n"

    return summary
