import os
from model_client import get_vertex_ai_model_client
from typing import Dict, Any, List
from google.cloud.aiplatform_v1beta1.types import HarmCategory, SafetyRating, SafetySetting

def check_safety(payload: Dict[str, Any], config: Dict[str, Any] = None) -> Dict[str, Any]:
    config = config or {}
    project_id = config.get("project_id") or os.environ.get("GOOGLE_CLOUD_PROJECT")
    location = config.get("location") or os.environ.get("GOOGLE_CLOUD_LOCATION")
    model_id = config.get("model_id") or "gemini-1.5-flash-001"

    vertex_ai = get_vertex_ai_model_client(project_id, location)

    text_to_check = payload.get("text", "")
    
    model = vertex_ai.preview.generative_models.GenerativeModel(model_id)
    
    # For safety attributes, we can set safety_settings in generate_content
    # The response will contain safety_ratings
    response = model.generate_content(
        contents=[{"role": "user", "parts": [{"text": text_to_check}]}],
        safety_settings=[
            SafetySetting(category=HarmCategory.HARM_CATEGORY_HATE_SPEECH, threshold=SafetySetting.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE),
            SafetySetting(category=HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT, threshold=SafetySetting.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE),
            SafetySetting(category=HarmCategory.HARM_CATEGORY_HARASSMENT, threshold=SafetySetting.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE),
            SafetySetting(category=HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT, threshold=SafetySetting.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE),
        ]
    )

    safety_attributes = []
    if response.prompt_feedback and response.prompt_feedback.safety_ratings:
        for rating in response.prompt_feedback.safety_ratings:
            safety_attributes.append({
                "category": HarmCategory(rating.category).name,
                "probability": SafetyRating.HarmProbability(rating.probability).name,
                "blocked": rating.is_blocked,
            })
    
    # Also check candidate safety if available
    if response.candidates and response.candidates[0].safety_ratings:
        for rating in response.candidates[0].safety_ratings:
            safety_attributes.append({
                "category": HarmCategory(rating.category).name,
                "probability": SafetyRating.HarmProbability(rating.probability).name,
                "blocked": rating.is_blocked,
            })

    return {"safety_attributes": safety_attributes}
