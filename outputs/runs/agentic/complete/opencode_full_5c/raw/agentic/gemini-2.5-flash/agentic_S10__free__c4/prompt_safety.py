import os
from google.cloud.aiplatform.generative_models import HarmCategory, HarmBlockThreshold
from model_client import get_vertex_ai_model
from model_models import LLMRequest, LLMResponse


def check_safety(text: str, model_id: str = "gemini-pro") -> dict:
    project_id = os.environ.get("GCP_PROJECT_ID")
    location = os.environ.get("GCP_LOCATION", "us-central1")
    model = get_vertex_ai_model(project_id, location, model_id)

    # Safety settings for generation
    safety_settings = {
        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    }

    # To check safety attributes, we can make a dummy generation request or use a specific API if available.
    # For simplicity and to demonstrate safety features, we'll try to generate content and inspect the response.
    # In a real scenario, you might want to call a dedicated safety API if available.
    try:
        response = model.generate_content(text, safety_settings=safety_settings)
        # If the content is blocked, the response will have a 'prompt_feedback' with 'block_reason'
        if response.prompt_feedback and response.prompt_feedback.block_reason:
            return {
                "is_safe": False,
                "block_reason": str(response.prompt_feedback.block_reason),
            }

        # If not blocked, we can still inspect safety attributes if they are available in the response
        # The Vertex AI SDK often includes safety attributes in the response if a dedicated safety API is not used.
        # This part might need adjustment based on the exact structure of the Vertex AI SDK response for safety scores.
        # For this example, we'll assume if it's not blocked, it's considered safe enough for this check.
        return {
            "is_safe": True,
            "safety_attributes": response.candidates[0].safety_ratings
            if response.candidates
            else None,
        }
    except Exception as e:
        # Handle cases where generation might fail due to safety reasons or other errors
        return {
            "is_safe": False,
            "error": str(e),
            "message": "Content might be unsafe or caused an API error.",
        }
