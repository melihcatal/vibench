from speech_client import get_azure_content_moderator_client
from speech_models import ModerationResult

def moderate_transcript_text(text: str) -> ModerationResult:
    client = get_azure_content_moderator_client()

    response = client.text_moderation.screen_text(
        text_content=text,
        language="eng", # Assuming English for this example
        autocorrect=True,
        pii=False, # Personal Identifiable Information
        list_id=None # Custom term list ID
    )
    
    is_profane = False
    review_recommended = False
    flagged_terms = []

    if response.terms:
        is_profane = True
        review_recommended = True
        for term_data in response.terms:
            flagged_terms.append(term_data.term)

    # Azure Content Moderator also provides a classification score, but screen_text primarily checks for terms and PII.
    # For a simple 'is_profane' check, `response.terms` is the most direct indicator. 
    # The service itself can recommend a human review based on its internal logic, which we infer if terms are found.

    return ModerationResult(
        original_text=text,
        is_profane=is_profane,
        review_recommended=review_recommended,
        terms=flagged_terms
    )
