import vertexai
from vertexai.preview.generative_models import GenerativeModel, HarmCategory, HarmBlockThreshold

def collect_model_output_and_metadata(project_id: str, location: str, model_name: str, prompt: str) -> dict:
    """Returns model output together with Google Cloud Vertex AI platform metadata."""
    vertexai.init(project=project_id, location=location)
    model = GenerativeModel(model_name)
    
    # Configure safety settings to ensure metadata includes safety attributes
    safety_settings = {
        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
    }

    response = model.generate_content(prompt, safety_settings=safety_settings)

    metadata = {
        "text": response.text,
        "finish_reason": response.candidates[0].finish_reason.name if response.candidates else None,
        "safety_attributes": []
    }
    
    if response.candidates:
        for rating in response.candidates[0].safety_ratings:
            metadata["safety_attributes"].append({
                "category": rating.category.name,
                "probability": rating.probability.name
            })
    
    # Add usage metadata if available (e.g., from a more detailed response object or a different API call)
    # The current GenerativeModel.generate_content response doesn't directly expose token usage easily
    # A more detailed integration might involve parsing raw REST responses or using client library features
    # that expose token counts. For now, we'll keep it simple with what's directly accessible.
    
    return metadata
