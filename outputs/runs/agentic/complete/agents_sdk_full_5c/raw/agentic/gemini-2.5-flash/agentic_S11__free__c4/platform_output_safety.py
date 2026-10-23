import vertexai
from vertexai.preview.language_models import TextGenerationModel
from typing import Dict, Any, Optional

def check_platform_output_safety(project_id: str, location: str, model_id: str, text: str) -> Dict[str, Any]:
    """Checks Google Cloud Vertex AI model output for unsafe content and returns safety attributes."
    # For this function, we assume the safety check happens as part of generation
    # or we can re-evaluate a piece of text if the model supports it directly.
    # As the Vertex AI TextGenerationModel.predict() already returns safety_attributes,
    # we will simulate fetching them or performing a new generation to get them.
    
    vertexai.init(project=project_id, location=location)
    model = TextGenerationModel.from_pretrained(model_id)
    
    # Re-generating to get safety attributes for a given text if not already available.
    # In a real scenario, you might pass the original response object if it contains safety info.
    response = model.predict(prompt=text)
    
    safety_attributes: Optional[Dict[str, Any]] = None
    if hasattr(response, 'safety_attributes') and response.safety_attributes:
        safety_attributes = response.safety_attributes.to_dict()
    
    return {
        "text": text,
        "safety_attributes": safety_attributes
    }
