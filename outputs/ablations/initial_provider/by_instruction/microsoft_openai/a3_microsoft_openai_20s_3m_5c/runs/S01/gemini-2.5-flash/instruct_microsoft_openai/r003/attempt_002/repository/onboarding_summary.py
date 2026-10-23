from identity_client import IdentityClient
from identity_models import SummarizeRequest, SummarizeResponse

def onboarding_summary(request: SummarizeRequest) -> SummarizeResponse:
    client = IdentityClient()

    if not client.aws_comprehend_client:
        raise ValueError("AWS Comprehend client not configured.")

    try:
        # AWS Comprehend doesn't have a direct 'summarize' API.
        # We will use 'detect_key_phrases' as a way to extract salient information
        # that can be used to construct a summary or provide key insights.
        response = client.aws_comprehend_client.detect_key_phrases(
            Text=request.text,
            LanguageCode="en" # Assuming onboarding text is in English
        )

        key_phrases = [phrase["Text"] for phrase in response["KeyPhrases"]]
        summary_text = "; ".join(key_phrases)

        if not summary_text:
            summary_text = "No key phrases detected for summarization."

        return SummarizeResponse(summary=summary_text)
    except Exception as e:
        raise RuntimeError(f"AWS Comprehend summarization failed: {e}")
