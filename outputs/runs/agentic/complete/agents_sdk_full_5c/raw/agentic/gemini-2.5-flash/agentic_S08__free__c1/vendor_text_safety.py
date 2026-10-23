import vertexai
from vertexai.preview.language_models import TextGenerationModel
import os
from typing import Dict, Any

def moderate_vendor_notes(text: str) -> Dict[str, Any]:
    """
    Moderates vendor notes or memo fields using Google Vertex AI (Gemini Pro) safety attributes.
    """
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    location = os.environ.get("VERTEX_AI_LOCATION", "us-central1")

    if not project_id:
        return {"error": "GOOGLE_CLOUD_PROJECT environment variable not set for Vertex AI.", "safety_attributes": {}}

    vertexai.init(project=project_id, location=location)
    
    # Using the gemini-pro model to get safety attributes
    # Although TextGenerationModel is used for text generation, predict() also returns safety attributes.
    model = TextGenerationModel.from_pretrained("gemini-pro")

    try:
        # Sending a dummy prompt to get safety attributes of the input text.
        # The actual generation response is less relevant here than the safety attributes.
        response = model.predict(prompt=text)
        
        # Extract safety attributes from the response
        safety_attributes = response._prediction_output.safety_attributes.to_dict() # Accessing internal representation
        
        # Process and simplify the safety attributes dictionary for easier consumption
        moderation_results = {
            "harm_categories": {},
            "is_flagged": False
        }

        if "categories" in safety_attributes and "scores" in safety_attributes:
            for i, category in enumerate(safety_attributes["categories"]):
                score = safety_attributes["scores"][i]
                blocked = safety_attributes.get("blocked", [False]*len(safety_attributes["categories"]))[i]
                moderation_results["harm_categories"][category] = {"score": score, "blocked": blocked}
                if blocked: # If any category is blocked, flag the text
                    moderation_results["is_flagged"] = True

        return {"moderation_results": moderation_results, "original_text": text}

    except Exception as e:
        return {"error": f"Error moderating text with Vertex AI: {e}", "safety_attributes": {}}
