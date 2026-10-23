import os
from google.cloud import language_v1


def summarize_transcription_results(transcription_result):
    """Summarize transcription results using Google Cloud Natural Language API."""
    client = language_v1.LanguageServiceClient()

    if isinstance(transcription_result, dict):
        transcript_text = transcription_result.get("full_transcript", "")
    elif hasattr(transcription_result, "full_transcript"):
        transcript_text = transcription_result.full_transcript
    else:
        transcript_text = str(transcription_result)

    if len(transcript_text) > 1000:
        sample_text = transcript_text[:1000]
    else:
        sample_text = transcript_text

    document = language_v1.Document(
        content=sample_text,
        type_=language_v1.Document.Type.PLAIN_TEXT,
    )

    response = client.analyze_entities(document=document)

    entities = []
    for entity in response.entities:
        entities.append(
            {
                "name": entity.name,
                "type": language_v1.Entity.Type(entity.type_).name,
                "salience": entity.salience,
            }
        )

    categories_response = client.classify_text(document=document)

    categories = []
    for category in categories_response.categories:
        categories.append({"name": category.name, "confidence": category.confidence})

    return {
        "text_length": len(transcript_text),
        "sample_analyzed": sample_text,
        "top_entities": sorted(entities, key=lambda x: x["salience"], reverse=True)[:5],
        "content_categories": categories,
        "entity_count": len(entities),
    }
