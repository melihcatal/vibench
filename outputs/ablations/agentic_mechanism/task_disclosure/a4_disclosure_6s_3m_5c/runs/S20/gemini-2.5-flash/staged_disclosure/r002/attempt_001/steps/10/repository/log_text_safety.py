import os
from google.cloud import language_v2

def check_text_for_safety(text_content):
    """
    Checks the given text content for unsafe content using Google Cloud Natural Language API.
    """
    client = language_v2.LanguageServiceClient()

    document = language_v2.Document(
        content=text_content,
        type_=language_v2.Document.Type.PLAIN_TEXT
    )

    # Use the moderateText method for safety checks
    response = client.moderate_text(document=document)

    # Return the moderation categories and their scores
    moderation_feedback = {}
    for category in response.moderation_categories:
        moderation_feedback[category.name] = category.score

    return moderation_feedback

if __name__ == "__main__":
    # Example usage:
    # Set the GOOGLE_APPLICATION_CREDENTIALS environment variable
    # For local development, ensure your GOOGLE_APPLICATION_CREDENTIALS points to a service account key file
    # os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/path/to/your/service_account_key.json"

    log_message = "This is a log message that might contain some problematic content like hate speech or harassment."
    safety_results = check_text_for_safety(log_message)

    print(f"Safety check results for log message: '{log_message}'")
    for category, score in safety_results.items():
        print(f"- {category}: {score}")

    log_message_clean = "This is a clean log message without any issues."
    safety_results_clean = check_text_for_safety(log_message_clean)

    print(f"
Safety check results for clean log message: '{log_message_clean}'")
    for category, score in safety_results_clean.items():
        print(f"- {category}: {score}")
