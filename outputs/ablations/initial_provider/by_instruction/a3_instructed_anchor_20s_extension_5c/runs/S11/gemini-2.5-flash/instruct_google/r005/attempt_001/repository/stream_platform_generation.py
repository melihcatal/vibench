from google.cloud import aiplatform
from typing import Iterator

def stream_platform_generation(project_id: str, location: str, model_name: str, prompt: str) -> Iterator[str]:
    """Streams output from a Google Vertex AI managed model.

    Args:
        project_id: The Google Cloud project ID.
        location: The Google Cloud region where the model is deployed.
        model_name: The name or ID of the model to invoke (e.g., "text-bison@001").
        prompt: The input prompt for the model.

    Returns:
        An iterator of strings, where each string is a chunk of the model's generated text.
    """
    aiplatform.init(project=project_id, location=location)
    model = aiplatform.TextGenerationModel.from_pretrained(model_name)
    responses = model.stream_predict(prompt)
    for response in responses:
        yield response.text
