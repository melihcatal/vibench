import vertexai
from vertexai.generative_models import GenerativeModel, Part, FinishReason

def stream_platform_generation(project_id: str, location: str, model_name: str, prompt: str):
    vertexai.init(project=project_id, location=location)
    model = GenerativeModel(model_name)
    responses = model.generate_content(
        prompt,
        stream=True
    )

    for response in responses:
        # The 'response' object itself is the provider's response object
        yield response
