from typing import Dict, Any
from model_client import load_platform_config
from model_models import GenerationRequest
from vertexai import init
from vertexai.generative_models import GenerativeModel, Content, Role, Part


def collect_platform_metadata(
    model_id: str, request: GenerationRequest
) -> Dict[str, Any]:
    config = load_platform_config()
    init(project=config["project_id"], location=config["location"])
    model = GenerativeModel(model_id)
    contents = []
    for msg in request.messages:
        role = Role.MODEL if msg.role == "assistant" else Role.USER
        contents.append(Content(role=role, parts=[Part.from_text(msg.content)]))
    response = model.generate_content(contents)
    metadata = {
        "content": str(response.text or ""),
        "usage_metadata": {
            "prompt_token_count": getattr(
                response.usage_metadata, "prompt_token_count", 0
            ),
            "candidates_token_count": getattr(
                response.usage_metadata, "candidates_token_count", 0
            ),
            "total_token_count": getattr(
                response.usage_metadata, "total_token_count", 0
            ),
        },
        "finish_reason": response.candidates[0].finish_reason.value
        if response.candidates
        else None,
        "model_handle": model.model_name,
        "resource_id": model_id,
    }
    return metadata
