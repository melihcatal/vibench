import os
from typing import Dict, Any
from google.cloud import aiplatform
from google.generativeai.types import HarmCategory, HarmBlockThreshold

from observability_models import SafetyCheckRequest

def check_log_safety(request: SafetyCheckRequest, project_id: str, location: str = "us-central1") -> Dict[str, Any]:
    aiplatform.init(project=project_id, location=location)

    # Use the specific model identifier for a text generation model
    model_id = os.environ.get("VERTEX_AI_GENERATIVE_MODEL_ID", "gemini-pro")
    model = aiplatform.preview.language_models.ChatModel.from_pretrained(model_id)

    # Configure safety settings. The actual implementation for safety checks
    # through the API might involve specific parameters or dedicated safety models.
    # For demonstration, we simulate checking by attempting generation with strict safety settings.
    # A real safety API would return specific scores or classifications.
    safety_settings = {
        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    }

    try:
        # Attempt to generate a response, if it's blocked, it means unsafe content was detected
        response = model.predict(prompt=f"Analyze the safety of the following text: {request.text}", safety_settings=safety_settings)
        # If no exception, it means the content passed the safety filters for generation context.
        # In a real scenario, a dedicated safety API would return more granular results.
        return {"is_safe": True, "details": "Content passed generative model's safety filters."}
    except Exception as e:
        # This catch is a simplification. Real safety APIs provide explicit safety ratings.
        # For Vertex AI, if the input itself triggers safety concerns, the prediction might fail
        # or return specific safety attributes in the response metadata.
        if "safety_ratings" in str(e):
             return {"is_safe": False, "details": f"Content was blocked by safety filters. Details: {e}"}
        else:
             return {"is_safe": False, "details": f"An error occurred during safety check: {e}"}
