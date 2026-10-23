import os
from google.cloud import language_v2

def check_for_unsafe_content(text_content: str):
    """
    Checks the given text content for unsafe content using Google Cloud's Natural Language API.

    Args:
        text_content: The text extracted from a document.

    Returns:
        A dictionary containing the moderation feedback.
    """
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set
    # or authenticate using another method supported by google-cloud-python.
    # For demonstration, we assume credentials are set up.

    client = language_v2.LanguageServiceClient()

    document = language_v2.Document(
        content=text_content,
        type_=language_v2.Document.Type.PLAIN_TEXT,
    )

    response = client.moderate_text(document=document)

    # The response contains categories and their confidence scores.
    # You can define a threshold for what you consider "unsafe".
    # For example, if any category has a score above 0.5, it might be flagged.
    moderation_feedback = {}
    for category_feedback in response.moderation_categories:
        moderation_feedback[category_feedback.category.name] = category_feedback.score

    return moderation_feedback

if __name__ == '__main__':
    # Example usage:
    text_to_check_safe = "This is a safe document with no harmful content."
    text_to_check_unsafe = "I hate you, you are stupid." # Example of potentially unsafe content

    print(f"Checking text: '{text_to_check_safe}'")
    safe_result = check_for_unsafe_content(text_to_check_safe)
    print(f"Moderation result: {safe_result}\n")

    print(f"Checking text: '{text_to_check_unsafe}'")
    unsafe_result = check_for_unsafe_content(text_to_check_unsafe)
    print(f"Moderation result: {unsafe_result}")
