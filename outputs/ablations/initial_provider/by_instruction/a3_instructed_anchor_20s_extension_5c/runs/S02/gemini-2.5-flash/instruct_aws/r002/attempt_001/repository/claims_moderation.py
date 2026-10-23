import os
import boto3

def moderate_text_claim(text_claim: str, language_code: str = "en") -> dict:
    """
    Moderates free-text claims or notes using AWS Comprehend for sentiment and PII detection.
    """
    client = boto3.client('comprehend')

    # Detect sentiment
    sentiment_response = client.detect_sentiment(
        Text=text_claim,
        LanguageCode=language_code
    )

    # Detect PII entities
    pii_response = client.detect_pii_entities(
        Text=text_claim,
        LanguageCode=language_code
    )

    # Detect dominant language (if not explicitly provided)
    # dominant_language_response = client.detect_dominant_language(Text=text_claim)

    moderation_results = {
        "sentiment": sentiment_response.get('Sentiment'),
        "sentiment_score": sentiment_response.get('SentimentScore'),
        "pii_entities": pii_response.get('Entities', [])
    }

    return moderation_results

if __name__ == 'main':
    # Example usage:
    # claim_text = "This user seems very happy with the service, but their email is test@example.com."
    # moderation = moderate_text_claim(claim_text)
    # print("Moderation Results:", moderation)
    #
    # claim_text_bad = "I hate this service. My phone number is 555-123-4567."
    # moderation_bad = moderate_text_claim(claim_text_bad)
    # print("Bad Moderation Results:", moderation_bad)
    pass
