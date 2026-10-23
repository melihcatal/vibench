from google.cloud import aiplatform
import os
from typing import Dict, Any, Optional


def check_log_message_safety(
    log_message: str, project_id: str = None, location: str = "us-central1"
) -> Optional[Dict[str, Any]]:
    """Checks a log message for unsafe content using Google Cloud Vertex AI (Gemini Pro safety attributes).

    Args:
        log_message: The text of the log message to check.
        project_id: The GCP project ID. If None, it will be inferred from the environment.
        location: The GCP region for Vertex AI. Default is 'us-central1'.

    Returns:
        A dictionary containing safety attributes and scores, or None if an error occurs.
    """
    if not log_message:
        return None

    if not project_id:
        project_id = os.getenv("GCP_PROJECT_ID")
        if not project_id:
            raise ValueError(
                "GCP_PROJECT_ID environment variable or project_id argument must be set."
            )

    # Initialize Vertex AI - Provider-identifying signal: aiplatform.init
    aiplatform.init(project=project_id, location=location)

    # Load the model - Provider-identifying signal: gemini-pro model ID
    model = aiplatform.GenerativeModel("gemini-pro")

    try:
        # Generating content with an empty prompt and just sending the text will trigger safety attributes check
        response = model.generate_content(
            log_message,
            safety_settings=[
                {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
                {
                    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                    "threshold": "BLOCK_NONE",
                },
                {
                    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                    "threshold": "BLOCK_NONE",
                },
            ],
        )

        # Safety attributes are available in the prompt_feedback.safety_attributes
        # Or if the response was blocked, in the candidates[0].safety_ratings
        if response.prompt_feedback and response.prompt_feedback.safety_ratings:
            safety_results = {
                rating.category.name: rating.probability.name
                for rating in response.prompt_feedback.safety_ratings
            }
            return safety_results
        elif response.candidates and response.candidates[0].safety_ratings:
            # If the response was blocked, safety_ratings might be on the candidate
            safety_results = {
                rating.category.name: rating.probability.name
                for rating in response.candidates[0].safety_ratings
            }
            return safety_results
        else:
            return {
                "message": "No explicit safety ratings returned.",
                "response_text_length": len(response.text),
            }

    except Exception as e:
        print(f"Error checking log message safety with Vertex AI: {e}")
        return None


if __name__ == "__main__":
    # Example Usage (requires GCP_PROJECT_ID env var and Vertex AI enabled)
    project_id = os.getenv("GCP_PROJECT_ID")
    if not project_id:
        print("Please set the GCP_PROJECT_ID environment variable to run this example.")
    else:
        safe_message = "User 'johndoe' updated their profile successfully."
        unsafe_message = (
            "This log message contains some very bad words and hateful content."
        )

        print(f"\n--- Checking safety for safe message: '{safe_message}' ---")
        safety_result_safe = check_log_message_safety(
            safe_message, project_id=project_id
        )
        print(safety_result_safe)

        print(
            f"\n--- Checking safety for potentially unsafe message: '{unsafe_message}' ---"
        )
        safety_result_unsafe = check_log_message_safety(
            unsafe_message, project_id=project_id
        )
        print(safety_result_unsafe)
