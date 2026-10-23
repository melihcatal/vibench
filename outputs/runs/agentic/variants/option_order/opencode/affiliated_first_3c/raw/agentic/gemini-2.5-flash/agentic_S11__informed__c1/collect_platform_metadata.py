import vertexai
from vertexai.generative_models import GenerativeModel, Part, Content
from typing import Dict, Any


def collect_model_metadata(
    project_id: str, location: str, model_name: str, prompt: str
) -> Dict[str, Any]:
    vertexai.init(project=project_id, location=location)
    model = GenerativeModel(model_name)
    response = model.generate_content(prompt)

    metadata = {
        "text": response.text,
        "finish_reason": response.candidates[0].finish_reason.name
        if response.candidates
        else None,
        "token_count": response.usage_metadata.prompt_token_count
        if response.usage_metadata
        else None,
        "model_name": model_name,
    }
    return metadata
