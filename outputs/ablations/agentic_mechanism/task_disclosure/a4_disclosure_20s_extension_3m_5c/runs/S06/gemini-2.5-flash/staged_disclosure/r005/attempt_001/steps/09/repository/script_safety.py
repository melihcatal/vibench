
from google.cloud import language_v2

def check_unsafe_content(text_content: str) -> dict:
    """Checks the given text for unsafe content using Google Cloud's Language AI.

    Args:
        text_content: The narration script content to check.

    Returns:
        A dictionary containing the moderation feedback.
    """
    client = language_v2.LanguageServiceClient()

    document = language_v2.Document(
        content=text_content, type_=language_v2.Document.Type.PLAIN_TEXT
    )

    # Available features: sentiment, entities, syntax, classification, moderateText
    # For this task, we only need moderateText.
    response = client.moderate_text(document=document)

    # The response will contain a list of moderation categories and their scores.
    # A score closer to 1.0 indicates a higher likelihood of unsafe content.
    return {
        "moderation_feedback": [
            {"category": category.name, "score": category.score}
            for category in response.moderation_categories
        ]
    }

if __name__ == "__main__":
    # Example usage:
    script_to_check_safe = "This is a safe and pleasant narration script."
    script_to_check_unsafe = "This script contains some potentially offensive language, like hate speech and slurs."

    print(f"Checking script: '{script_to_check_safe}'")
    safe_result = check_unsafe_content(script_to_check_safe)
    print(f"Moderation result: {safe_result}\n")

    print(f"Checking script: '{script_to_check_unsafe}'")
    unsafe_result = check_unsafe_content(script_to_check_unsafe)
    print(f"Moderation result: {unsafe_result}\n")
