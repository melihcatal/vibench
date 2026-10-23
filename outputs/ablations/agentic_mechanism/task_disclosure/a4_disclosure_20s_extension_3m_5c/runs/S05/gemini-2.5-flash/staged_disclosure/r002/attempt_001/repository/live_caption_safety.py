import os
from google.cloud import language_v1

def check_unsafe_content(text_content):
    """
    Checks live transcript text for unsafe content using Google Cloud Natural Language API.
    Note: For comprehensive safety checks (e.g., hate speech, profanity), a dedicated content moderation API
    like Google's Perspective API would be more appropriate. This example uses Natural Language API
    for sentiment and entity analysis as a general text analysis example.
    """

    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set for authentication
    # os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/path/to/your/service-account-key.json"

    client = language_v1.LanguageServiceClient()

    document = language_v1.Document(content=text_content, type_=language_v1.Document.Type.PLAIN_TEXT)

    # Perform sentiment analysis
    sentiment = client.analyze_sentiment(request={"document": document}).document_sentiment
    
    # Perform entity analysis
    entities = client.analyze_entities(request={"document": document}).entities

    # You can define your own logic here to determine "unsafe" based on sentiment and entities.
    # For example, extremely negative sentiment could be flagged.
    # More advanced logic would involve integrating with a proper content moderation service.
    
    is_unsafe = False
    safety_details = []

    if sentiment.score < -0.5 and sentiment.magnitude > 1.0: # Example threshold for very negative sentiment
        is_unsafe = True
        safety_details.append(f"Strongly negative sentiment detected (score: {sentiment.score}, magnitude: {sentiment.magnitude}).")

    # Example: Check for specific entities that might be considered sensitive
    sensitive_keywords = ["violence", "threat", "harm", "hate"]
    for entity in entities:
        for keyword in sensitive_keywords:
            if keyword in entity.name.lower():
                is_unsafe = True
                safety_details.append(f"Potentially sensitive entity '{entity.name}' detected.")
                break
    
    return {
        "is_unsafe": is_unsafe,
        "safety_details": safety_details,
        "sentiment": {"score": sentiment.score, "magnitude": sentiment.magnitude},
        "entities": [{"name": entity.name, "type": language_v1.Entity.Type(entity.type_).name, "salience": entity.salience} for entity in entities]
    }

if __name__ == "__main__":
    # Example usage:
    text_to_check = "I am so happy today! This is a wonderful experience."
    result = check_unsafe_content(text_to_check)
    print(f"Text: '{text_to_check}'")
    print(f"Safety Check Result: {result}")

    text_to_check_2 = "I hate this. This is terrible and I want to hurt someone."
    result_2 = check_unsafe_content(text_to_check_2)
    print(f"
Text: '{text_to_check_2}'")
    print(f"Safety Check Result: {result_2}")
