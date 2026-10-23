import os
import vertexai
from vertexai.preview.language_models import TextGenerationModel
from observability_models import LogSafetyCheckRequest, LogSafetyCheckResponse

def check_log_text_safety(request: LogSafetyCheckRequest) -> LogSafetyCheckResponse:
    """Checks selected log message text for unsafe content using Vertex AI's PaLM 2 for Text."""
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    location = os.getenv("GCP_REGION", "us-central1") # Choose an appropriate region for Vertex AI

    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")

    vertexai.init(project=project_id, location=location)
    model = TextGenerationModel.from_pretrained("text-bison")

    prompt = f"""
    Analyze the following log message for any unsafe content, including but not limited to:
    harassment, hate speech, sexually explicit content, dangerous content, or personally identifiable information (PII).
    
    Log Message: "{request.log_message_text}"
    
    Respond with "SAFE" if no unsafe content is found.
    If unsafe content is found, respond with "UNSAFE" followed by a comma-separated list of categories of unsafe content detected (e.g., "UNSAFE, PII, HARASSMENT")
    and a brief explanation for each category.
    """

    parameters = {
        "temperature": 0.1,
        "max_output_tokens": 200,
        "top_p": 0.8,
        "top_k": 40
    }

    try:
        response = model.predict(prompt, **parameters)
        response_text = response.text.strip().upper()

        if response_text.startswith("SAFE"):
            return LogSafetyCheckResponse(is_safe=True)
        elif response_text.startswith("UNSAFE"):
            parts = response_text.split(",", 1)
            reasons = []
            is_safe = True
            if len(parts) > 1:
                is_safe = False
                # Attempt to parse categories and explanations
                # This parsing can be complex, for this example we'll take the raw text as reasons
                reasons.append(parts[1].strip())
            return LogSafetyCheckResponse(is_safe=is_safe, reasons=reasons)
        else:
            return LogSafetyCheckResponse(is_safe=False, reasons=["Could not determine safety from model response."])

    except Exception as e:
        print(f"Error checking log safety: {e}")
        return LogSafetyCheckResponse(is_safe=False, reasons=[f"Failed to check safety due to an error: {e}"])

if __name__ == "__main__":
    # Example usage
    safe_log_request = LogSafetyCheckRequest(
        log_message_text="User 'john.doe' successfully updated profile.",
        language_code="en"
    )
    unsafe_log_request_pii = LogSafetyCheckRequest(
        log_message_text="Error: User's credit card number 1234-5678-9012-3456 expired.",
        language_code="en"
    )
    unsafe_log_request_harmful = LogSafetyCheckRequest(
        log_message_text="Detected an attack attempt from IP 192.168.1.1. Malicious script: <script>alert('xss')</script>",
        language_code="en"
    )
    unsafe_log_request_toxic = LogSafetyCheckRequest(
        log_message_text="A very rude user commented 'You are all idiots!' on post 123.",
        language_code="en"
    )

    try:
        print("\n--- Safety Check: Safe Log ---")
        response_safe = check_log_text_safety(safe_log_request)
        print(f"Log: '{safe_log_request.log_message_text}'")
        print(f"Is Safe: {response_safe.is_safe}")
        print(f"Reasons: {response_safe.reasons}")

        print("\n--- Safety Check: Unsafe Log (PII) ---")
        response_unsafe_pii = check_log_text_safety(unsafe_log_request_pii)
        print(f"Log: '{unsafe_log_request_pii.log_message_text}'")
        print(f"Is Safe: {response_unsafe_pii.is_safe}")
        print(f"Reasons: {response_unsafe_pii.reasons}")
        
        print("\n--- Safety Check: Unsafe Log (Harmful Script) ---")
        response_unsafe_harmful = check_log_text_safety(unsafe_log_request_harmful)
        print(f"Log: '{unsafe_log_request_harmful.log_message_text}'")
        print(f"Is Safe: {response_unsafe_harmful.is_safe}")
        print(f"Reasons: {response_unsafe_harmful.reasons}")

        print("\n--- Safety Check: Unsafe Log (Toxic) ---")
        response_unsafe_toxic = check_log_text_safety(unsafe_log_request_toxic)
        print(f"Log: '{unsafe_log_request_toxic.log_message_text}'")
        print(f"Is Safe: {response_unsafe_toxic.is_safe}")
        print(f"Reasons: {response_unsafe_toxic.reasons}")

    except ValueError as e:
        print(f"Error: {e}")
        print("Please ensure GOOGLE_CLOUD_PROJECT and GCP_REGION environment variables are set.")
