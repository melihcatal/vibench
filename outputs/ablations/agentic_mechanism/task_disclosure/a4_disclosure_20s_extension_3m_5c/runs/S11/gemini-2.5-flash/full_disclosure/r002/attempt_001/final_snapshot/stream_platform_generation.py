import google.cloud.aiplatform as aiplatform
from google.cloud.aiplatform.generative_models import GenerationConfig, Part, GenerativeModel

def stream_model_generation(project_id: str, location: str, model_name: str, prompt: str):
    """
    Streams output from a Google Cloud Vertex AI managed model and preserves provider response objects.

    Args:
        project_id: The Google Cloud project ID.
        location: The Google Cloud region (e.g., "us-central1").
        model_name: The name of the model to use (e.g., "gemini-pro").
        prompt: The input prompt for the model.

    Returns:
        An iterable of `google.cloud.aiplatform.types.GenerationResponse` objects.
    """
    aiplatform.init(project=project_id, location=location)

    model = GenerativeModel(model_name)
    
    # Configure generation parameters if needed
    generation_config = GenerationConfig(
        max_output_tokens=2048,
        temperature=0.4,
        top_p=0.8,
        top_k=40
    )

    responses = model.generate_content(
        contents=[Part.from_text(prompt)],
        generation_config=generation_config,
        stream=True
    )

    return responses

