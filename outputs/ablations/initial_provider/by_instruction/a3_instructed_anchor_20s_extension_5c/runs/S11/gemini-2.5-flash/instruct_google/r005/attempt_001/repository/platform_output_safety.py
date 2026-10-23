from google.cloud import aiplatform
from typing import Dict, Any

def check_platform_output_safety(project_id: str, location: str, model_name: str, prompt: str) -> Dict[str, Any]:
    """Checks Google Vertex AI model output for unsafe content.

    Args:
        project_id: The Google Cloud project ID.
        location: The Google Cloud region where the model is deployed.
        model_name: The name or ID of the model to invoke (e.g., "text-bison@001").
        prompt: The input prompt for the model to generate content.

    Returns:
        A dictionary containing safety attributes and scores from the model response.
    """
    aiplatform.init(project=project_id, location=location)
    model = aiplatform.TextGenerationModel.from_pretrained(model_name)
    response = model.predict(prompt)
    # Assuming safety attributes are part of the prediction response or content_filter_results
    # This might vary based on the specific model and API version.
    # For text-bison@001, safety attributes are typically in response.candidates[0].safety_attributes
    safety_attributes = {}
    if response.candidates and hasattr(response.candidates[0], 'safety_attributes'):
        safety_attributes = response.candidates[0].safety_attributes._asdict()
    return safety_attributes
