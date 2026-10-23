from model_client import load_platform_config
from model_models import (
    GenerationRequest,
    GenerationResponse,
    Message,
    GenerationMetadata,
)
from vertexai import init
from vertexai.generative_models import (
    GenerativeModel,
    GenerationConfig,
    Content,
    Role,
    Part,
)


def invoke_platform_model(
    model_id: str, request: GenerationRequest
) -> GenerationResponse:
    config = load_platform_config()
    init(project=config["project_id"], location=config["location"])
    model = GenerativeModel(model_id)
    contents = []
    for msg in request.messages:
        role = Role.MODEL if msg.role == "assistant" else Role.USER
        contents.append(Content(role=role, parts=[Part.from_text(msg.content)]))
    generation_config = GenerationConfig(
        temperature=request.temperature,
        max_output_tokens=request.max_output_tokens,
    )
    response = model.generate_content(contents, generation_config=generation_config)
    metadata = GenerationMetadata(
        prompt_token_count=getattr(response.usage_metadata, "prompt_token_count", 0),
        candidates_token_count=getattr(
            response.usage_metadata, "candidates_token_count", 0
        ),
        total_token_count=getattr(response.usage_metadata, "total_token_count", 0),
    )
    return GenerationResponse(content=str(response.text or ""), metadata=metadata)
