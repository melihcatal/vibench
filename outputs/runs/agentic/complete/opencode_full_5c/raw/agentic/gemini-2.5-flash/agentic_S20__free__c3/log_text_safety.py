import os
from typing import Dict, Any
from google.cloud import aiplatform
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
from observability_models import SafetyCheckRequest

# Ensure GOOGLE_CLOUD_PROJECT environment variable is set
PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
if not PROJECT_ID:
    raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")

# Initialize Vertex AI SDK
aiplatform.init(
    project=PROJECT_ID, location="us-central1"
)  # Choose an appropriate region
genai.configure(project=PROJECT_ID)


def check_log_text_safety(request: SafetyCheckRequest) -> Dict[str, Any]:
    try:
        # Using a generative model for safety checks, specifically for content moderation.
        # This leverages the safety features built into models like Gemini.
        model = genai.GenerativeModel("gemini-1.0-pro")

        # Attempt to generate content with the given text and strict safety settings.
        # If the content is flagged, an exception or an empty response may occur,
        # or the response object will contain safety attributes.
        response = model.generate_content(
            request.text,
            safety_settings={
                HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
                HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
                HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
                HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
            },
        )

        # Check if the response was blocked due to safety concerns
        if not response._result.candidates:
            # If no candidates, it means the content was blocked
            safety_ratings = response._result.prompt_feedback.safety_ratings
            blocked_categories = []
            for rating in safety_ratings:
                if rating.blocked:
                    blocked_categories.append(
                        rating.category.name.replace("HARM_CATEGORY_", "")
                    )
            return {
                "is_safe": False,
                "blocked_categories": blocked_categories,
                "raw_safety_ratings": [r.to_dict() for r in safety_ratings],
            }
        else:
            # Content was not blocked, return that it's safe and include the safety ratings
            safety_ratings = response._result.candidates[0].safety_ratings
            return {
                "is_safe": True,
                "blocked_categories": [],
                "raw_safety_ratings": [r.to_dict() for r in safety_ratings],
            }

    except Exception as e:
        # Catch any other exceptions, e.g., API errors, and report them.
        return {"is_safe": False, "error": f"Error during safety check: {e}"}


if __name__ == "__main__":
    # Example usage:
    safe_text_request = SafetyCheckRequest(
        text="User logged in successfully with IP 192.168.1.1."
    )
    safe_result = check_log_text_safety(safe_text_request)
    print("\n--- Safety Check Result (Safe Text) ---")
    print(safe_result)

    # Example of potentially unsafe text (replace with actual test cases as needed)
    # Note: The model's actual blocking behavior can vary.
    unsafe_text_request = SafetyCheckRequest(
        text="This log contains some very offensive language."
    )
    unsafe_result = check_log_text_safety(unsafe_text_request)
    print("\n--- Safety Check Result (Potentially Unsafe Text) ---")
    print(unsafe_result)
