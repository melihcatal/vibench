from google.cloud import language_v1
import os

def summarize_message(text: str) -> dict:
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)

    # Analyze sentiment for a basic summary indication
    sentiment = client.analyze_sentiment(request={'document': document}).document_sentiment

    # Analyze entities to extract key information
    entities = client.analyze_entities(request={'document': document}).entities

    summary = {
        "sentiment": {
            "score": sentiment.score,
            "magnitude": sentiment.magnitude
        },
        "entities": [{
            "name": entity.name,
            "type": language_v1.Entity.Type(entity.type_).name,
            "salience": entity.salience
        } for entity in entities]
    }
    return summary


if __name__ == "__main__":
    example_message = "The customer reported a critical issue with order #54321. They are very unhappy."
    summary_result = summarize_message(example_message)
    print(f"Message Summary: {summary_result}")
