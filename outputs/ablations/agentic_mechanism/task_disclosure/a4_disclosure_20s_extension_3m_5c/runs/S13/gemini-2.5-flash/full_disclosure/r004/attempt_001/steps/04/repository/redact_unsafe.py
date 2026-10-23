import os
from azure.cognitiveservices.vision.contentmoderator import ContentModeratorClient
from msrest.authentication import CognitiveServicesCredentials

def redact_unsafe_text(text: str) -> str:
    """
    Flags or redacts unsafe spans from text using Azure Content Moderator.
    """
    # Azure Content Moderator configuration
    SUBSCRIPTION_KEY = os.environ.get("AZURE_CONTENT_MODERATOR_SUBSCRIPTION_KEY")
    ENDPOINT = os.environ.get("AZURE_CONTENT_MODERATOR_ENDPOINT")

    if not SUBSCRIPTION_KEY or not ENDPOINT:
        raise ValueError("Azure Content Moderator subscription key and endpoint must be set as environment variables.")

    client = ContentModeratorClient(
        endpoint=ENDPOINT,
        credentials=CognitiveServicesCredentials(SUBSCRIPTION_KEY)
    )

    # Screen the text for profanity and other unsafe content
    screen_result = client.text_moderation.screen_text(
        text_content=text,
        language="eng",
        autocorrect=False,
        classify=False
    )

    # For simplicity, this example redacts all found terms.
    # More sophisticated logic could flag or apply different redaction strategies.
    redacted_text = list(text)
    if screen_result.terms:
        for term in screen_result.terms:
            # The API returns 0-based indices
            start_index = term.index
            end_index = term.original_index + len(term.term)
            for i in range(start_index, end_index):
                if i < len(redacted_text):
                    redacted_text[i] = '*'
    
    return "".join(redacted_text)

