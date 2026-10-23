from google.cloud import aiplatform
from vertexai.preview.generative_models import GenerativeModel, HarmCategory, HarmBlockThreshold
from typing import Dict, Any

def check_text_safety(text_content: str) -> Dict[str, Any]:
    aiplatform.init()
    model = GenerativeModel("gemini-pro") # Using Gemini Pro for content moderation

    # No specific generation is needed, just evaluating safety attributes
    # We send the text as content and let the model evaluate its safety
    response = model.generate_content(
        text_content,
        safety_settings={
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.HARM_BLOCK_THRESHOLD_UNSPECIFIED,
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.HARM_BLOCK_THRESHOLD_UNSPECIFIED,
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.HARM_BLOCK_THRESHOLD_UNSPECIFIED,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.HARM_BLOCK_THRESHOLD_UNSPECIFIED,
        }
    )

    # The safety attributes are usually part of the candidate's safety_ratings
    safety_ratings = []
    if response.candidates:
        for candidate in response.candidates:
            if candidate.safety_ratings:
                safety_ratings.extend([{'category': rating.category.name, 'probability': rating.probability.name} for rating in candidate.safety_ratings])
    
    return {"safety_ratings": safety_ratings}
