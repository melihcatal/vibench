import os
from google.cloud import language_v2 # Provider-identifying signal: google-cloud-language

def redact_unsafe_text(text: str) -> str:
    """
    Flags or redacts unsafe spans from text using Google Cloud's Language AI.
    """
    client = language_v2.LanguageServiceClient()

    document = language_v2.Document(
        content=text,
        type_=language_v2.Document.Type.PLAIN_TEXT
    )

    moderation_response = client.moderate_text(document=document)
    
    redacted_text = list(text)
    
    for moderation_category in moderation_response.moderation_categories:
        if moderation_category.category == language_v2.ModerationCategory.Category.UNSPECIFIED:
            continue
        if moderation_category.score > 0.5: # Example threshold for "unsafe"
            for span in moderation_category.inline_token_offsets:
                start = span.start_offset
                end = span.end_offset
                for i in range(start, end):
                    redacted_text[i] = '*' # Redact the unsafe span
                    
    return "".join(redacted_text)
