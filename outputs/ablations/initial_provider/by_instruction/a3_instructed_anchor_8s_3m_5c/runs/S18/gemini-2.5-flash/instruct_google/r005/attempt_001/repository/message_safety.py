from google.cloud import language_v1
import os

def check_message_safety(text: str) -> dict:
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)

    # Classify text into categories to identify potentially unsafe content
    # Note: This is a general categorization and not a dedicated content moderation API.
    # For dedicated content moderation, other services or custom models might be needed.
    response = client.classify_text(request={'document': document})
    categories = [{
        "name": category.name,
        "confidence": category.confidence
    } for category in response.categories]

    # Additionally, check sentiment for extreme negativity as an indicator
    sentiment = client.analyze_sentiment(request={'document': document}).document_sentiment

    safety_check = {
        "categories": categories,
        "sentiment_score": sentiment.score,
        "is_potentially_unsafe": any(cat["name"].startswith("/Violence") or cat["name"].startswith("/Illicit Goods") for cat in categories) or sentiment.score < -0.5 # Example heuristic
    }
    return safety_check


if __name__ == "__main__":
    example_unsafe_message = "I will harm you. This is a threat."
    safety_result_unsafe = check_message_safety(example_unsafe_message)
    print(f"Safety Check (Unsafe): {safety_result_unsafe}")

    example_safe_message = "Hello, how are you today?"
    safety_result_safe = check_message_safety(example_safe_message)
    print(f"Safety Check (Safe): {safety_result_safe}")
