from model_client import get_comprehend_client
from model_models import SafetyCheckRequest, SafetyCheckResponse
import os


def check_output_safety(request: SafetyCheckRequest) -> SafetyCheckResponse:
    """
    Check platform model output for unsafe content using Amazon Comprehend Toxicity Detection.
    """
    client = get_comprehend_client()

    response = client.detect_toxic_content(
        TextSegments=[{"Text": request.text}],
        LanguageCode="en",  # Assuming English for this example
    )
    return SafetyCheckResponse(response)


if __name__ == "__main__":
    # Example usage:
    # Ensure AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION are set in environment variables
    # Comprehend Toxicity Detection is part of Amazon Comprehend, make sure it's enabled for your region.
    safe_text_request = SafetyCheckRequest(
        text="The quick brown fox jumps over the lazy dog."
    )
    safe_response = check_output_safety(safe_text_request)
    print(f"Safe text safety labels: {safe_response.labels}")

    unsafe_text_request = SafetyCheckRequest(text="I hate you and I will hurt you.")
    unsafe_response = check_output_safety(unsafe_text_request)
    print(f"Unsafe text safety labels: {unsafe_response.labels}")
