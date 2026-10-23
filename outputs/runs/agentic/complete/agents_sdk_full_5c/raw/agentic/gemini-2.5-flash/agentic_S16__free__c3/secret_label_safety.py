import os
from google.cloud import language_v1
from typing import Dict, Any

def check_secret_labels_for_safety(text_to_analyze: str) -> Dict[str, Any]:
    """
    Checks given text (e.g., secret labels or notes) for unsafe content using Google Cloud Natural Language API.
    This example uses sentiment analysis as a proxy for 'safety' for demonstration.
    A more robust safety check would involve entity extraction, custom classification, or content moderation APIs.
    """
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(content=text_to_analyze, type_=language_v1.Document.Type.PLAIN_TEXT)

    # Perform sentiment analysis
    sentiment = client.analyze_sentiment(request={"document": document}).document_sentiment

    # Perform entity analysis
    entities_response = client.analyze_entities(request={"document": document})
    entities = [{"name": entity.name, "type": language_v1.Entity.Type(entity.type_).name} for entity in entities_response.entities]

    # You could define 'unsafe' based on sentiment score, or detected entity types
    # For this example, we'll just return the raw sentiment and entities.
    safety_results = {
        "text_analyzed": text_to_analyze,
        "sentiment_score": sentiment.score,
        "sentiment_magnitude": sentiment.magnitude,
        "entities": entities,
        "is_potentially_unsafe": bool(sentiment.score < -0.2 or len(entities) > 5) # Example heuristic
    }
    return safety_results

if __name__ == "__main__":
    # Example usage with some dummy text
    label_text_good = "This is a benign label for a production secret."
    label_text_bad = "Warning: This secret contains highly sensitive PII, handle with extreme care!"

    print("Checking good label text:")
    results_good = check_secret_labels_for_safety(label_text_good)
    print(f"  Results: {results_good}")

    print("\nChecking bad label text:")
    results_bad = check_secret_labels_for_safety(label_text_bad)
    print(f"  Results: {results_bad}")

    # Example with secret notes
    secret_notes = "User 'admin' changed this secret on 2023-10-27 due to a security incident. Review logs."
    print("\nChecking secret notes:")
    results_notes = check_secret_labels_for_safety(secret_notes)
    print(f"  Results: {results_notes}")
