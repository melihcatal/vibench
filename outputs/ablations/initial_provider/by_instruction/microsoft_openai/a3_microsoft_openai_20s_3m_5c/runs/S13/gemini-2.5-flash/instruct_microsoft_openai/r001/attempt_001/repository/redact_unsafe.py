import os
from azure.cognitiveservices.vision.contentmoderator import ContentModeratorClient
from azure.cognitiveservices.vision.contentmoderator.models import EvaluateInput
from msrest.authentication import CognitiveServicesCredentials
from safety_models import RedactionRequest, RedactionResponse

def redact_unsafe(request: RedactionRequest) -> RedactionResponse:
    """
    Flags or redacts unsafe spans from text using Azure Content Moderator.
    """
    # Azure Content Moderator client setup
    SUBSCRIPTION_KEY = os.environ.get("AZURE_CONTENT_MODERATOR_KEY")
    ENDPOINT = os.environ.get("AZURE_CONTENT_MODERATOR_ENDPOINT")
    
    if not SUBSCRIPTION_KEY or not ENDPOINT:
        raise ValueError("Azure Content Moderator key and endpoint must be set in environment variables.")

    client = ContentModeratorClient(
        endpoint=ENDPOINT,
        credentials=CognitiveServicesCredentials(SUBSCRIPTION_KEY)
    )

    # Use the Screen Text API for redaction and profanity detection
    # The SDK's text.screen_text function can mark profanity and PII
    # For direct redaction, we'd typically send content and then process the response to redact
    # The SDK provides detected terms, but actual redaction logic is often client-side or requires specific API features.
    # For this example, we'll simulate redaction based on detected terms if the API provides character offsets.
    
    # In Content Moderator SDK, screen_text returns a `Screen` object.
    # This object contains properties like `Pii` and `Terms`.
    # For direct redaction, often a separate API call or manual string replacement is needed based on offsets.
    # The provided SDK doesn't directly return a redacted string with a single call in this manner for general unsafe content.
    # We will simulate redaction for profanity as an example.

    screen_result = client.text_mod.screen_text(
        text_content_type="text/plain",
        text_content=request.text,
        language="eng",
        autocorrect=False,
        urls=False,
        pii=False
    )
    
    redacted_text = list(request.text) # Convert to list to allow easy character replacement
    flagged_categories = {}

    if screen_result.terms:
        for term in screen_result.terms:
            # Content Moderator terms provide index and original_index
            # We'll replace detected terms with asterisks for redaction
            start_index = term.index
            end_index = term.index + len(term.term)
            for i in range(start_index, end_index):
                if i < len(redacted_text):
                    redacted_text[i] = '*'
            flagged_categories["profanity"] = True # A general category for detected terms

    return RedactionResponse(
        redacted_text="".join(redacted_text),
        flagged_categories=flagged_categories
    )
