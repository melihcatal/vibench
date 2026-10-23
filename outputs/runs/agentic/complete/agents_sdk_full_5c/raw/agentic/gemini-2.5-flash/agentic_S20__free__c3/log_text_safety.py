import os
from google.cloud import aiplatform

def check_log_text_safety(
    log_message_text: str,
    project_id: str = None,
    location: str = "us-central1",
    model_name: str = "gemini-pro"
) -> dict:
    """Checks log message text for unsafe content using Google Cloud Vertex AI (Generative AI) safety features."""

    if project_id is None:
        project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
        if not project_id:
            raise ValueError("project_id must be provided or GOOGLE_CLOUD_PROJECT env var set.")

    aiplatform.init(project=project_id, location=location)
    model = aiplatform.GenerativeModel(model_name)

    print(f"Checking log text safety with Vertex AI model {model_name}...")
    try:
        # The safety attributes are usually part of the response if the model detects issues.
        # We'll rely on the model's built-in safety filters.
        response = model.generate_content(log_message_text, safety_settings=None)
        
        # Accessing safety attributes from the response
        safety_attributes = {
            "blocked": response.candidates[0].safety_ratings is not None and len(response.candidates[0].safety_ratings) > 0 and any(rating.blocked for rating in response.candidates[0].safety_ratings),
            "safety_ratings": [
                {"category": rating.category.name, "probability": rating.probability.name, "blocked": rating.blocked}
                for rating in response.candidates[0].safety_ratings
            ] if response.candidates and response.candidates[0].safety_ratings else []
        }

        return {
            "input_text": log_message_text,
            "is_safe": not safety_attributes["blocked"],
            "safety_details": safety_attributes
        }

    except Exception as e:
        print(f"Error checking log text safety: {e}")
        return {
            "input_text": log_message_text,
            "is_safe": False,
            "safety_details": {"error": str(e), "blocked": True, "safety_ratings": []}
        }

if __name__ == "__main__":
    # Example usage:
    # Set GOOGLE_CLOUD_PROJECT environment variable before running
    # export GOOGLE_CLOUD_PROJECT="your-gcp-project-id"
    # Ensure Vertex AI API is enabled and you have necessary permissions.
    
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    if project_id:
        print("\n--- Checking a safe log message ---")
        safe_log = "User 'johndoe' successfully logged in from 192.168.1.10."
        safety_result = check_log_text_safety(safe_log, project_id=project_id)
        print(f"Log: '{safety_result['input_text']}'")
        print(f"Is Safe: {safety_result['is_safe']}")
        print(f"Safety Details: {safety_result['safety_details']}")

        print("\n--- Checking a potentially unsafe log message (e.g., with personal identifiable information or sensitive content) ---")
        # Disclaimer: This example uses a placeholder for potentially unsafe content.
        # Actual detection depends on the LLM's safety filters.
        unsafe_log = "Urgent! Customer with SSN XXX-XX-1234 reported an issue. Address: 123 Main St. Bank Account: 5678."
        safety_result = check_log_text_safety(unsafe_log, project_id=project_id)
        print(f"Log: '{safety_result['input_text']}'")
        print(f"Is Safe: {safety_result['is_safe']}")
        print(f"Safety Details: {safety_result['safety_details']}")

        print("\n--- Checking another safe log message ---")
        another_safe_log = "Process ID 1234 completed task 'data_export' in 150ms."
        safety_result = check_log_text_safety(another_safe_log, project_id=project_id)
        print(f"Log: '{safety_result['input_text']}'")
        print(f"Is Safe: {safety_result['is_safe']}")
        print(f"Safety Details: {safety_result['safety_details']}")

    else:
        print("Please set the GOOGLE_CLOUD_PROJECT environment variable.")
