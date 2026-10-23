from google.cloud import language_v1
from google.cloud.language_v1 import enums


def moderate_transcript_text(transcript_text):
    """Moderate transcript text before publishing using Google Cloud Natural Language API."""
    client = language_v1.LanguageServiceClient()

    document = language_v1.Document(
        content=transcript_text, type_=enums.Document.Type.PLAIN_TEXT
    )

    response = client.analyze_sentiment(document=document)

    moderation_results = {
        "overall_sentiment": {
            "score": response.document_sentiment.score,
            "magnitude": response.document_sentiment.magnitude,
        },
        "sentences": [],
    }

    for sentence in response.sentences:
        sentence_info = {
            "text": sentence.text.content,
            "sentiment_score": sentence.sentiment.score,
            "sentiment_magnitude": sentence.sentiment.magnitude,
        }

        if abs(sentence.sentiment.score) > 0.8:
            sentence_info["needs_review"] = True
            sentence_info["reason"] = "Strong emotional content"
        elif sentence.sentiment.magnitude > 2.0:
            sentence_info["needs_review"] = True
            sentence_info["reason"] = "High emotional intensity"
        else:
            sentence_info["needs_review"] = False

        moderation_results["sentences"].append(sentence_info)

    toxicity_response = client.analyze_entity_sentiment(document=document)

    entities = []
    for entity in toxicity_response.entities:
        if entity.sentiment.score < -0.5:
            entities.append(
                {
                    "name": entity.name,
                    "type": enums.Entity.Type(entity.type_).name,
                    "sentiment_score": entity.sentiment.score,
                    "salience": entity.salience,
                    "needs_review": True,
                }
            )

    moderation_results["problematic_entities"] = entities

    return moderation_results


if __name__ == "__main__":
    transcript = "This product is terrible and I hate it. The service was awful."
    results = moderate_transcript_text(transcript)
    print(f"Moderation results: {results}")
