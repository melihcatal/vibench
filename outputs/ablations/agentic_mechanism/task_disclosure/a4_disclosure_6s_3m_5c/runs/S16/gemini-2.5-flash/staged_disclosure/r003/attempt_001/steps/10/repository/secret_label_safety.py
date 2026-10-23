import os
from google.cloud import language_v1

def check_safety(text_content: str) -> dict:
    """
    Checks the given text for unsafe content using Google Cloud Natural Language API.

    Args:
        text_content: The text to be analyzed for safety.

    Returns:
        A dictionary containing the moderation scores.
    """
    client = language_v1.LanguageServiceClient()

    document = language_v1.Document(
        content=text_content, type_=language_v1.Document.Type.PLAIN_TEXT
    )

    # Available categories for moderation can be found in the documentation:
    # https://cloud.google.com/natural-language/docs/moderating-text
    response = client.moderate_text(document=document)

    result = {}
    for category_score in response.moderation_categories:
        result[category_score.name] = category_score.score

    return result

if __name__ == "__main__":
    # Example usage:
    # Set up GOOGLE_APPLICATION_CREDENTIALS environment variable
    # e.g., export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/keyfile.json"

    # Example 1: Safe text
    safe_text = "This is a secret label for a project about cloud computing."
    print(f"Safety check for '{safe_text}': {check_safety(safe_text)}")

    # Example 2: Potentially unsafe text (replace with actual test cases)
    # The API will score different categories of potentially unsafe content.
    # Note: Replace with content that you want to test against moderation policies.
    # For demonstration, a neutral string is used.
    unsafe_text = "I hate this project, it is terrible."
    print(f"Safety check for '{unsafe_text}': {check_safety(unsafe_text)}")
