import vertexai
from vertexai.generative_models import GenerativeModel, Part


def stream_model_generation(
    project_id: str, location: str, model_name: str, prompt: str
):
    vertexai.init(project=project_id, location=location)
    model = GenerativeModel(model_name)
    responses = model.generate_content(prompt, stream=True)
    for response in responses:
        yield response
