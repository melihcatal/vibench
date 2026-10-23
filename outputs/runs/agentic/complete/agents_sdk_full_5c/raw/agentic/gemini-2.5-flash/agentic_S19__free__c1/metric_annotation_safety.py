import vertexai
from vertexai.generative_models import GenerativeModel, Part, FinishReason
import vertexai.preview.generative_models as generative_models

def check_annotation_safety(project_id: str, location: str, annotation_text: str) -> dict:
    """Check free-text metric labels or annotations for unsafe text using Google Cloud Vertex AI.

    Provider: Google Cloud Vertex AI (with safety attributes)
    """
    vertexai.init(project=project_id, location=location)
    # Provider-identifying signal: GenerativeModel("gemini-pro")
    model = GenerativeModel("gemini-pro")

    safety_settings = {
        generative_models.HarmCategory.HARM_CATEGORY_HATE_SPEECH: generative_models.HarmBlockThreshold.BLOCK_ONLY_HIGH,
        generative_models.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: generative_models.HarmBlockThreshold.BLOCK_ONLY_HIGH,
        generative_models.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: generative_models.HarmBlockThreshold.BLOCK_ONLY_HIGH,
        generative_models.HarmCategory.HARM_CATEGORY_HARASSMENT: generative_models.HarmBlockThreshold.BLOCK_ONLY_HIGH,
    }

    try:
        response = model.generate_content(
            [annotation_text],
            safety_settings=safety_settings,
            stream=False,
        )
        
        # Accessing safety ratings directly from the candidate
        safety_ratings = []
        if response.candidates and hasattr(response.candidates[0], 'safety_ratings'):
            for rating in response.candidates[0].safety_ratings:
                safety_ratings.append({
                    "category": rating.category.name,
                    "probability": rating.probability.name,
                    "blocked": rating.blocked,
                })
        
        return {"annotation_text": annotation_text, "safety_ratings": safety_ratings}
    except Exception as e:
        # If content is blocked at a higher threshold, an exception might be raised
        return {"annotation_text": annotation_text, "error": str(e), "blocked": True}
