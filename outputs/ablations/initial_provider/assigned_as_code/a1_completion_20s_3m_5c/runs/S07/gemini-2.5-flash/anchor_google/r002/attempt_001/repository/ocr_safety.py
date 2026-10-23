from typing import Dict, Any, List
from document_client import DocumentClient
from document_models import OcrSafetyResult
from google.cloud import aiplatform
import vertexai.preview.generative_models as generative_models

def ocr_safety(payload: Dict[str, Any], config: Dict[str, Any]) -> Dict[str, Any]:
    project_id = config["project_id"]
    location = config["location"]

    client = DocumentClient(project_id, location)
    aiplatform_client = client.aiplatform_client

    text_to_check = payload["text"]

    # Initialize the generative model (e.g., Gemini Pro)
    model = aiplatform_client.GenerativeModel("gemini-pro")

    # Define safety settings for content moderation
    safety_settings = {
        generative_models.HarmCategory.HARM_CATEGORY_HATE_SPEECH: generative_models.HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
        generative_models.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: generative_models.HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
        generative_models.HarmCategory.HARM_CATEGORY_HARASSMENT: generative_models.HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
        generative_models.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: generative_models.HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
    }

    response_safety: List[OcrSafetyResult] = []

    try:
        # Generate content with safety settings
        response = model.generate_content(
            text_to_check,
            safety_settings=safety_settings,
            generation_config=generative_models.GenerationConfig(candidate_count=1)
        )

        # Analyze safety attributes from the response (if available and structured this way)
        # Note: The actual structure of safety attributes in the response might vary based on API version
        # and model. This is an illustrative example.
        if response.prompt_feedback and response.prompt_feedback.safety_ratings:
            for rating in response.prompt_feedback.safety_ratings:
                response_safety.append(OcrSafetyResult(
                    category=str(rating.category).split('.')[-1],  # e.g., HARM_CATEGORY_HATE_SPEECH
                    probability=rating.probability_score if hasattr(rating, 'probability_score') else 0.0 # Placeholder, actual API might have different scoring
                ))
        
        # If no explicit safety ratings are returned but the content was blocked, we can infer a high safety risk.
        if not response_safety and response.prompt_feedback and response.prompt_feedback.block_reason:
             response_safety.append(OcrSafetyResult(
                category="BLOCKED",
                probability=1.0 # High probability of being unsafe if blocked
            ))


    except Exception as e:
        # Handle cases where safety check fails or content is blocked directly by the model
        response_safety.append(OcrSafetyResult(
            category="ERROR",
            probability=1.0  # Indicate an error or high uncertainty
        ))
        print(f"Safety check failed: {e}")

    return {"safety_results": response_safety}
