import vertexai
from vertexai.generative_models import GenerativeModel, Part


def collect_platform_metadata(
    project_id: str, location: str, model_name: str, prompt: str
):
    vertexai.init(project=project_id, location=location)
    model = GenerativeModel(model_name)
    response = model.generate_content(prompt)
    metadata = {
        "model_name": model_name,
        "project_id": project_id,
        "location": location,
        "finish_reason": response.candidates[0].finish_reason.name
        if response.candidates
        else None,
        "token_count": response.usage_metadata.prompt_token_count
        if response.usage_metadata
        else None,
    }
    return response.text, metadata
