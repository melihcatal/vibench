from vertexai.preview.generative_models import GenerativeModel
import vertexai

def stream_platform_generation(project_id: str, location: str, model_name: str, prompt: str):
    """
    Streams output from a Google Cloud Vertex AI generative model.
    """
    vertexai.init(project=project_id, location=location)
    model = GenerativeModel(model_name)
    responses = model.generate_content(
        prompt,
        stream=True,
        generation_config={"max_output_tokens": 256},
    )
    
    # Iterate and yield each part of the streaming response
    for response in responses:
        yield response
