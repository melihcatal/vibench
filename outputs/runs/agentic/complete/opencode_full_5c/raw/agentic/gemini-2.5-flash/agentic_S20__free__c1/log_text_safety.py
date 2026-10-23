import os
from typing import List
from google.cloud import aiplatform
from observability_client import ObservabilityClient # for conceptual integration
from observability_models import SafetyCheckResult

PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT")
LOCATION = "us-central1"  # Example region for Vertex AI

def check_log_safety(log_message: str) -> SafetyCheckResult:
    aiplatform.init(project=PROJECT_ID, location=LOCATION)

    # Using a pre-trained model for text generation, which includes safety filters
    # Provider Identification: aiplatform.TextGenerationModel and specific model_id
    model = aiplatform.GenerativeModel("gemini-pro")

    # The safety check is implicitly handled by the model's content moderation capabilities.
    # We prompt the model to identify if the content is unsafe.
    prompt = f"""
    Analyze the following log message for any unsafe content, such as hate speech, self-harm, sexual content, or violence.
    Respond with 'SAFE' if no unsafe content is found, otherwise respond with 'UNSAFE' and provide specific reasons.

    Log message: """{log_message}"""
    """

    response = model.generate_content(prompt)
    response_text = response.text.strip()

    is_safe = "UNSAFE" not in response_text.upper()
    reasons = []
    if not is_safe:
        # Attempt to extract reasons if the model explicitly provides them
        if ":" in response_text:
            reasons = [response_text.split(":", 1)[1].strip()]
        else:
            reasons = [response_text]

    return SafetyCheckResult(
        is_safe=is_safe,
        reasons=reasons
    )

if __name__ == "__main__":
    # Example usage:
    safe_message = "User 'johndoe' logged in successfully from IP 192.168.1.100."
    unsafe_message = "Detected potential SQL injection attempt from malicious_user on /login endpoint."
    another_unsafe_message = "User provided sensitive personal data in a public comment: My SSN is 123-45-6789."

    result1 = check_log_safety(safe_message)
    print(f"\n--- Safety Check for \"{safe_message}\" ---")
    print(f"Is Safe: {result1.is_safe}")
    print(f"Reasons: {result1.reasons}")

    result2 = check_log_safety(unsafe_message)
    print(f"\n--- Safety Check for \"{unsafe_message}\" ---")
    print(f"Is Safe: {result2.is_safe}")
    print(f"Reasons: {result2.reasons}")

    result3 = check_log_safety(another_unsafe_message)
    print(f"\n--- Safety Check for \"{another_unsafe_message}\" ---")
    print(f"Is Safe: {result3.is_safe}")
    print(f"Reasons: {result3.reasons}")
