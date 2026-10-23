import os
import vertexai
from vertexai.preview.generative_models import GenerativeModel, HarmCategory, HarmBlockThreshold

def check_safety(text: str, project_id: str, location: str = "us-central1") -> dict:
    """Checks text for unsafe content using Google Cloud Vertex AI GenerativeModel safety features."""
    vertexai.init(project=project_id, location=location)
    model = GenerativeModel("gemini-pro") # Using a general purpose Gemini model

    # Configure safety settings to block content at various thresholds
    safety_settings = [
        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    ]

    try:
        response = model.generate_content(
            text,
            safety_settings=safety_settings,
            request_options={"timeout": 120}
        )
        # If content is blocked, access the prompt_feedback.safety_ratings
        if response.prompt_feedback and response.prompt_feedback.safety_ratings:
            safety_scores = [
                {"category": rating.category.name, "probability": rating.probability.name}
                for rating in response.prompt_feedback.safety_ratings
            ]
            return {"is_safe": False, "safety_ratings": safety_scores}
        else:
            return {"is_safe": True, "safety_ratings": []}
    except Exception as e:
        # If the generation itself fails due to safety, it might raise an exception
        return {"is_safe": False, "error": str(e), "safety_ratings": []}

if __name__ == '__main__':
    _project_id = os.environ.get("GCP_PROJECT_ID", "your-gcp-project-id") # Replace with your project ID
    _location = "us-central1"

    _safe_text = "The quick brown fox jumps over the lazy dog."
    _result_safe = check_safety(_safe_text, _project_id, _location)
    print(f"Text: '{_safe_text}', Safety Result: {_result_safe}")

    # Example of potentially unsafe content (adjust as needed for testing, be cautious)
    _unsafe_text = "I will harm myself."
    _result_unsafe = check_safety(_unsafe_text, _project_id, _location)
    print(f"Text: '{_unsafe_text}', Safety Result: {_result_unsafe}")
