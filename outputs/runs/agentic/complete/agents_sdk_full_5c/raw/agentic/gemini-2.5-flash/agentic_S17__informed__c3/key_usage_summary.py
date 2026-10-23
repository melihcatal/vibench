import os
import google.generativeai as genai
from security_client import configure_gemini_api, get_gemini_model
from security_models import SummarizationRequest, SummarizationResponse

def summarize_key_usage(request: SummarizationRequest) -> SummarizationResponse:
    """Summarizes key usage and crypto events using Google Gemini API."""
    configure_gemini_api()
    model = get_gemini_model("gemini-pro") # Using gemini-pro for text summarization

    prompt = (
        f"Summarize the following key usage and crypto events log. Focus on key activity, type of operations, and any anomalies. "
        f"Keep the summary concise, within {request.max_output_tokens} tokens.\n\n"
        f"Events:\n{request.text_to_summarize}"
    )

    response = model.generate_content(prompt)
    
    # The generated content is usually in parts, join them if multiple.
    summary = "".join([part.text for part in response.candidates[0].content.parts])

    return SummarizationResponse(summary_text=summary)

if __name__ == '__main__':
    # Example Usage
    # Ensure GOOGLE_API_KEY environment variable is set.

    sample_key_events = """
    [2023-10-26 10:00:01] Key: app-enc-key, Operation: Encrypt, Status: Success, User: service-account-dev
    [2023-10-26 10:00:05] Key: auth-sign-key, Operation: Sign, Status: Success, User: service-account-auth
    [2023-10-26 10:01:10] Key: app-enc-key, Operation: Decrypt, Status: Success, User: service-account-dev
    [2023-10-26 10:02:15] Key: audit-key, Operation: Encrypt, Status: Success, User: auditor-service
    [2023-10-26 10:03:00] Key: app-enc-key, Operation: Decrypt, Status: Failure, Error: InvalidCiphertext, User: service-account-dev
    [2023-10-26 10:03:05] Key: app-enc-key, Operation: Decrypt, Status: Failure, Error: PermissionDenied, User: malicious-user
    [2023-10-26 10:04:00] Key: auth-sign-key, Operation: Verify, Status: Success, User: public-api-gateway
    """

    try:
        print("Summarizing key usage events with Google Gemini API...")
        request = SummarizationRequest(text_to_summarize=sample_key_events, max_output_tokens=150)
        response = summarize_key_usage(request)
        print("\n--- Key Usage Summary ---")
        print(response.summary_text)
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
