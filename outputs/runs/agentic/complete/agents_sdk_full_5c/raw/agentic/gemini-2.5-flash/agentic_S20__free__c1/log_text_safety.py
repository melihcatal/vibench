import os
import vertexai
from vertexai.preview.generative_models import GenerativeModel
from typing import Dict, Any

def check_log_text_safety(log_message: str, project_id: str, location: str = "us-central1") -> Dict[str, Any]:
    """Checks selected log message text for unsafe content using Vertex AI Generative Model safety attributes."""
    vertexai.init(project=project_id, location=location)
    model = GenerativeModel("gemini-pro") # Using Gemini Pro for content moderation

    print(f"Checking log message for safety: '{log_message[:50]}...'")

    # When calling generate_content, safety attributes are automatically included in the response
    # for models that support it, like Gemini Pro.
    response = model.generate_content(log_message, safety_settings={})
    
    safety_attributes = {
        "sexual_content": "UNKNOWN",
        "hate_speech": "UNKNOWN",
        "harassment": "UNKNOWN",
        "dangerous_content": "UNKNOWN"
    }

    if response.candidates and response.candidates[0].safety_ratings:
        for rating in response.candidates[0].safety_ratings:
            safety_attributes[rating.category.name.lower()] = rating.probability.name.lower()

    return safety_attributes

if __name__ == '__main__':
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        print("GOOGLE_CLOUD_PROJECT environment variable not set.")
        exit(1)

    test_messages = [
        "User provided offensive input: you are an idiot!",
        "Successfully processed user request with ID 12345.",
        "Found a potential SQL injection attempt in parameter 'q'.",
        "This log contains some very strong language which might be considered explicit."
    ]

    print("\n--- Log Text Safety Checks ---")
    for msg in test_messages:
        safety_report = check_log_text_safety(msg, project_id)
        print(f"\nMessage: '{msg}'")
        print(f"Safety Report: {safety_report}")
