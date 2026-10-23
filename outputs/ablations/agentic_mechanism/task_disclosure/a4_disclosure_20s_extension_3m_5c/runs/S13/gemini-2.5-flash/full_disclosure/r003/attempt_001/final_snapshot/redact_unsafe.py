import os
from google.cloud import language_v2

def redact_unsafe_text(text_content: str) -> str:
    """Redacts unsafe spans from the given text using Google Cloud Natural Language API."""

    client = language_v2.LanguageServiceClient()

    document = language_v2.Document(
        content=text_content,
        type_=language_v2.Document.Type.PLAIN_TEXT
    )

    # Use the moderate_text method for content moderation
    response = client.moderate_text(document=document)

    redacted_text = list(text_content)
    # The Google Cloud Natural Language API (language_v2) does not directly provide span offsets for unsafe content
    # like some other moderation APIs. For true redaction based on specific unsafe spans, a more advanced
    # approach would be needed, potentially involving custom logic or a different API that provides
    # character offsets for detected unsafe categories.

    # For the purpose of this example, we'll demonstrate a conceptual "flagging"
    # or simple redaction if a high-level category is detected.
    # In a real-world scenario, you would iterate through categories and their scores
    # and decide on redaction strategies based on thresholds and specific category types.

    # This is a simplified example. A more robust solution would involve
    # iterating through the moderation categories and their confidence scores
    # to determine which parts of the text to redact based on specific
    # unsafe content categories and their corresponding character offsets
    # if the API provided them.

    # Since language_v2.moderate_text gives category scores for the whole document,
    # and not specific spans, this function will conceptually "redact" by
    # replacing the entire text with a placeholder if any category exceeds a
    # simple threshold. For actual span-based redaction, more detailed
    # span information from the moderation API would be required.

    # Placeholder for actual redaction logic if span information were available
    # For now, if any category is flagged as "unsafe" (above a simple threshold),
    # we'll return a generic redacted message.

    # Example threshold for demonstration purposes
    UNSAFE_THRESHOLD = 0.8

    for category_filter in response.moderation_categories:
        if category_filter.score > UNSAFE_THRESHOLD and category_filter.name != "Medical": # Exclude "Medical" for this example
            return "[REDACTED UNSAFE CONTENT]"

    return text_content
