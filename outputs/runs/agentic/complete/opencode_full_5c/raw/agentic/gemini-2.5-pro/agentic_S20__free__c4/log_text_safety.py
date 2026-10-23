import os
from observability_client import get_generative_model_client
from observability_models import ContentSafetyRequest, ContentSafetyResponse


def check_log_safety(request: ContentSafetyRequest) -> ContentSafetyResponse:
    """
    Checks log message text for unsafe content (like PII or secrets)
    using Google's Gemini model. This is a basic check.
    """
    model = get_generative_model_client(model_name="gemini-1.5-flash-001")

    prompt = f"""
    Analyze the following log message for sensitive content.
    Does it contain any Personally Identifiable Information (PII) like names,
    emails, phone numbers, or any credentials like API keys or passwords?

    Respond with only 'SAFE' or 'UNSAFE'. If UNSAFE, list the reasons why on new lines.

    Log Message: "{request.text}"
    """

    response = model.generate_content(prompt)

    lines = response.text.strip().split("\n")
    decision = lines[0].upper()

    if decision == "UNSAFE":
        reasons = (
            lines[1:] if len(lines) > 1 else ["Unspecified sensitive content detected."]
        )
        return ContentSafetyResponse(is_safe=False, reasons=reasons)

    return ContentSafetyResponse(is_safe=True)


if __name__ == "__main__":
    if os.environ.get("GCP_PROJECT_ID"):
        safe_log = ContentSafetyRequest(text="User 12345 updated their profile.")
        unsafe_log = ContentSafetyRequest(
            text="Error processing for user john.doe@example.com, API Key: sk-123abc456def."
        )

        safe_result = check_log_safety(safe_log)
        print(f"Log: '{safe_log.text}' -> Safe: {safe_result.is_safe}")

        unsafe_result = check_log_safety(unsafe_log)
        print(
            f"Log: '{unsafe_log.text}' -> Safe: {unsafe_result.is_safe}, Reasons: {unsafe_result.reasons}"
        )
    else:
        print("GCP_PROJECT_ID environment variable not set. Skipping example run.")
