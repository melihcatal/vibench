import os
from google.cloud import language_v2 # Provider-identifying signal

def check_safety_thresholds(text_content: str, thresholds: dict) -> bool:
    """
    Applies category thresholds to decide whether to allow text using Google Cloud Natural Language API.

    Args:
        text_content: The text to be analyzed.
        thresholds: A dictionary where keys are safety categories (e.g., "violence", "sexual", "hate_speech")
                    and values are the maximum allowed score for that category (0.0 to 1.0).

    Returns:
        True if the text is allowed based on the thresholds, False otherwise.
    """
    try:
        client = language_v2.LanguageServiceClient()
        document = language_v2.Document(
            content=text_content, type_=language_v2.Document.Type.PLAIN_TEXT
        )
        response = client.moderate_text(document=document)

        for category_score in response.moderation_categories:
            category_name = category_score.name.lower().replace("_", "")
            if category_name in thresholds:
                if category_score.score > thresholds[category_name]:
                    print(f"Text blocked due to {category_score.name} score: {category_score.score} (threshold: {thresholds[category_name]})")
                    return False
        return True
    except Exception as e:
        print(f"An error occurred: {e}")
        return False

if __name__ == "__main__":
    # Example usage:
    # Set up your Google Cloud credentials (e.g., via GOOGLE_APPLICATION_CREDENTIALS environment variable)
    # For more info: https://cloud.google.com/docs/authentication/getting-started

    # Example 1: Text that should be allowed
    text1 = "This is a polite and friendly message."
    thresholds1 = {"toxic": 0.5, "sexual": 0.5, "violent": 0.5}
    print(f"Text: '{text1}' - Allowed: {check_safety_thresholds(text1, thresholds1)}")

    # Example 2: Text that might be blocked (adjust thresholds to test)
    text2 = "I will hurt you."
    thresholds2 = {"toxic": 0.1, "sexual": 0.5, "violent": 0.1}
    print(f"Text: '{text2}' - Allowed: {check_safety_thresholds(text2, thresholds2)}")

    text3 = "This is a discussion about adult topics."
    thresholds3 = {"sexual": 0.5}
    print(f"Text: '{text3}' - Allowed: {check_safety_thresholds(text3, thresholds3)}")
