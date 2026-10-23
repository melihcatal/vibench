import vertexai
from vertexai.language_models import TextGenerationModel

def check_platform_output_safety(project_id: str, location: str, model_name: str, prompt: str):
    """Checks platform model output for unsafe content using provider-specific safety attributes."""
    vertexai.init(project=project_id, location=location)
    model = TextGenerationModel.from_pretrained(model_name)
    response = model.predict(prompt=prompt)

    safety_attributes = response.safety_attributes.to_dict() if response.safety_attributes else None

    # Example: Check if any category has a high severity score
    is_safe = True
    if safety_attributes and 'categories' in safety_attributes and 'scores' in safety_attributes:
        for i, score in enumerate(safety_attributes['scores']):
            # Assuming a threshold for unsafe content (e.g., score > 0.8)
            if score > 0.8:
                is_safe = False
                break

    return {
        "text": response.text,
        "safety_attributes": safety_attributes,
        "is_safe": is_safe
    }
