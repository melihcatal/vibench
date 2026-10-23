from identity_client import AWSClient
from identity_models import OnboardingSummaryRequest, OnboardingSummaryResponse

def onboarding_summary(request: OnboardingSummaryRequest) -> OnboardingSummaryResponse:
    aws_client = AWSClient()
    comprehend_client = aws_client.get_comprehend_client()

    try:
        # Using detect_key_phrases as a form of summarization for the onboarding data.
        # For more advanced summarization, a more complex NLP model or a service like Amazon SageMaker
        # hosting a summarization model would be used.
        response = comprehend_client.detect_key_phrases(
            Text=request.onboarding_data,
            LanguageCode='en' # Assuming English for now
        )
        key_phrases = [phrase['Text'] for phrase in response['KeyPhrases']]
        summary = ". ".join(key_phrases)

        return OnboardingSummaryResponse(summary=summary)
    except Exception as e:
        return OnboardingSummaryResponse(summary=f"Summarization failed: {str(e)}")
