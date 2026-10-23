import vertexai
from vertexai.generative_models import GenerativeModel

def stream_vertex_ai_generation(project_id: str, location: str, model_name: str, prompt: str):
    vertexai.init(project=project_id, location=location)
    model = GenerativeModel(model_name)
    responses = model.generate_content(prompt, stream=True)
    for response in responses:
        yield response  # Yield the raw provider response object
