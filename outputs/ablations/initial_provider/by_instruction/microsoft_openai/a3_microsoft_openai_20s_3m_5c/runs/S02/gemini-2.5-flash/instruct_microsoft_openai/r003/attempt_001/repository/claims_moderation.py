import os
from google.cloud import language_v1
from typing import Dict, Any, List

def moderate_text_claims(text: str) -> Dict[str, Any]:
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set
    # pointing to your service account key file.
    try:
        client = language_v1.LanguageServiceClient()
    except Exception as e:
        print(f"Error initializing Google Cloud Natural Language client: {e}. Ensure GOOGLE_APPLICATION_CREDENTIALS is set.")
        return {"error": str(e)}

    document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)

    # Detect sentiment
    sentiment = client.analyze_sentiment(request={'document': document}).document_sentiment
    
    # Detect entities
    entities_response = client.analyze_entities(request={'document': document})
    entities = [{'name': entity.name, 'type': language_v1.Entity.Type(entity.type_).name} for entity in entities_response.entities]

    # Detect content classification (requires auto_classify_text to be enabled in the API)
    # This part might require a different API call or configuration, focusing on sentiment and entities for moderation.
    # For direct content moderation, you might use other GCP APIs like Cloud Content Safety or implement custom logic.

    moderation_results = {
        "sentiment_score": sentiment.score,
        "sentiment_magnitude": sentiment.magnitude,
        "entities": entities,
        "moderation_notes": []
    }

    # Simple moderation logic based on sentiment for demonstration
    if sentiment.score < -0.5 and sentiment.magnitude > 1.0:
        moderation_results["moderation_notes"].append("Highly negative sentiment detected.")
    elif sentiment.score < -0.2:
        moderation_results["moderation_notes"].append("Negative sentiment detected.")

    return moderation_results

if __name__ == "__main__":
    # Example usage: Set GOOGLE_APPLICATION_CREDENTIALS environment variable
    # os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/path/to/your/service-account-key.json"

    test_claim_positive = "The user provided excellent feedback and was very satisfied."
    test_claim_negative = "This user repeatedly violated terms and exhibited abusive behavior."
    test_claim_neutral = "The user logged in successfully and updated their profile."

    print("\n--- Moderating Positive Claim ---")
    results_positive = moderate_text_claims(test_claim_positive)
    print(results_positive)

    print("\n--- Moderating Negative Claim ---")
    results_negative = moderate_text_claims(test_claim_negative)
    print(results_negative)

    print("\n--- Moderating Neutral Claim ---")
    results_neutral = moderate_text_claims(test_claim_neutral)
    print(results_neutral)
