import os
from google.cloud import language_v2

def check_unsafe_content(text: str) -> language_v2.ModerateTextResponse:
    """
    Checks localized copy for unsafe content using Google Cloud Language AI's ModerateText.

    Args:
        text: The localized copy string to check.

    Returns:
        A ModerateTextResponse object containing the moderation results.
    """
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set
    # or authenticate otherwise for Google Cloud client library to work.
    # For example: export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/keyfile.json"

    client = language_v2.LanguageServiceClient()

    document = language_v2.Document(
        content=text,
        type_=language_v2.Document.Type.PLAIN_TEXT
    )

    response = client.moderate_text(document=document)
    return response

