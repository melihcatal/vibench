import os
from google.cloud import aiplatform

def invoke_platform_model(
    project_id: str,
    location: str,
    model_id: str,
    prompt: str,
    temperature: float = 0.7,
    max_output_tokens: int = 200,
) -> str:
    """Invokes a provider-managed model (Google Cloud Vertex AI) through a platform client.

    Args:
        project_id: The Google Cloud project ID.
        location: The Google Cloud region (e.g., "us-central1").
        model_id: The ID of the model to invoke (e.g., "text-bison").
        prompt: The input prompt for the model.
        temperature: The sampling temperature for the model.
        max_output_tokens: The maximum number of tokens to generate.

    Returns:
        The model's generated text output.
    """
    aiplatform.init(project=project_id, location=location)

    # Initialize the GenerativeModel class for text models
    model = aiplatform.language_models.TextGenerationModel.from_pretrained(model_id)

    response = model.predict(
        prompt=prompt,
        temperature=temperature,
        max_output_tokens=max_output_tokens,
    )
    return response.text

