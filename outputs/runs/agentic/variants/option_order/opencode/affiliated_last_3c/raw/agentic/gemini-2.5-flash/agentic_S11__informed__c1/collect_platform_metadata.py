import os
import vertexai
from vertexai.preview.generative_models import GenerativeModel, Part


def collect_platform_metadata(
    project_id: str, location: str, model_name: str, prompt: str
):
    vertexai.init(project=project_id, location=location)
    model = GenerativeModel(model_name)
    response = model.generate_content(prompt)
    return {
        "text": response.text,
        "finish_reason": response.candidates[0].finish_reason,
        "token_usage": response.usage_metadata.prompt_token_count,
        "model_name": model_name,
    }
