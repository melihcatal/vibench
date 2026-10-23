from google.cloud import aiplatform
from google.cloud.aiplatform.schema.predict.prediction import TextGenerationPredictionResult

def collect_platform_metadata(project_id: str, location: str, model_name: str, prompt: str) -> TextGenerationPredictionResult:
    """Invokes a Google Vertex AI model and returns the full response object including metadata.

    Args:
        project_id: The Google Cloud project ID.
        location: The Google Cloud region where the model is deployed.
        model_name: The name or ID of the model to invoke (e.g., "text-bison@001").
        prompt: The input prompt for the model.

    Returns:
        The full TextGenerationPredictionResult object from Google Vertex AI, including metadata.
    """
    aiplatform.init(project=project_id, location=location)
    model = aiplatform.TextGenerationModel.from_pretrained(model_name)
    response = model.predict(prompt)
    return response
