import os
from typing import List, Dict, Any, Optional
from google.cloud import aiplatform
from google.api_core.client_options import ClientOptions

def check_log_message_safety(log_message_text: str, project_id: Optional[str] = None, location: str = "us-central1") -> Dict[str, Any]:
    """
    Checks selected log message text for unsafe content using Google Cloud Generative AI safety features.

    Args:
        log_message_text (str): The log message text to check for safety.
        project_id (Optional[str]): The Google Cloud Project ID. If None, it will be read from GOOGLE_CLOUD_PROJECT env var.
        location (str): The Google Cloud region for the AI Platform endpoint. Defaults to "us-central1".

    Returns:
        Dict[str, Any]: A dictionary containing safety attributes and scores. Returns an empty dict if an error occurs.
    """
    if not log_message_text:
        return {"safety_check_status": "skipped", "reason": "Empty log message text provided."}

    if project_id is None:
        project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
        if not project_id:
            raise ValueError("Google Cloud Project ID not provided and GOOGLE_CLOUD_PROJECT environment variable not set.")

    # Initialize AI Platform client
    client_options = ClientOptions(api_endpoint=f"{location}-aiplatform.googleapis.com")
    aiplatform.init(project=project_id, location=location, client_options=client_options)

    # Load the generative model with safety settings
    # Using gemini-pro as an example; ensure it's available in your region
    model = aiplatform.preview.language_models.GenerativeModel("gemini-pro")

    try:
        # The safety attributes are usually part of the response metadata or the content filter results
        # For direct safety checking, we might need to craft a prompt or rely on underlying model features.
        # As of current SDK, direct exposure of safety scores for arbitrary text input is not explicitly a separate API call
        # but rather part of content generation responses. We can simulate it by asking the model to evaluate safety.
        prompt = (
            "Analyze the following log message for any unsafe content, "
            "such as hate speech, sexually explicit content, harmful content, or dangerous content. "
            "Respond with a JSON object indicating categories and a safety score (e.g., safe, moderate, unsafe) for each.\n\n"
            f"Log Message: '{log_message_text}'\n\n"
            "JSON Output:"
        )

        response = model.generate_content(prompt)
        # Attempt to parse the response as JSON. The model is prompted to return JSON.
        try:
            safety_results = json.loads(response.text)
            print("Successfully performed safety check on log message.")
            return {"safety_check_status": "completed", "results": safety_results}
        except json.JSONDecodeError:
            print(f"Warning: Could not decode JSON from model response. Raw response: {response.text}")
            return {"safety_check_status": "completed", "raw_response": response.text, "note": "Model did not return valid JSON."}

    except Exception as e:
        print(f"Error performing safety check on log message: {e}")
        return {"safety_check_status": "failed", "error": str(e)}

if __name__ == "__main__":
    import json
    # Example usage:
    # Set GOOGLE_CLOUD_PROJECT environment variable
    # os.environ["GOOGLE_CLOUD_PROJECT"] = "your-gcp-project-id"

    safe_log = "User 'johndoe' successfully accessed resource '/data/reports'."
    unsafe_log_example = "Alert: Detected a threat attempt from IP 192.168.1.1. Malicious payload 'DROP TABLE users;' detected."
    another_unsafe_log = "Harmful content: User posted offensive comments in chat."

    print("\n--- Checking Safe Log ---")
    safe_check_results = check_log_message_safety(safe_log)
    print(json.dumps(safe_check_results, indent=2))

    print("\n--- Checking Potentially Unsafe Log (SQL Injection) ---")
    unsafe_check_results_sql = check_log_message_safety(unsafe_log_example)
    print(json.dumps(unsafe_check_results_sql, indent=2))

    print("\n--- Checking Potentially Unsafe Log (Offensive Content) ---")
    unsafe_check_results_offensive = check_log_message_safety(another_unsafe_log)
    print(json.dumps(unsafe_check_results_offensive, indent=2))
