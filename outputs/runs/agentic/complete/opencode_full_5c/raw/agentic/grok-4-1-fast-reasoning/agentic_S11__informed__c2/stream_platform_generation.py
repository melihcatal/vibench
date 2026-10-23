from typing import Generator
from model_client import load_platform_config
from model_models import GenerationRequest
from vertexai import init
from vertexai.generative_models import (
    GenerativeModel,
    GenerationConfig,
    Content,
    Role,
    Part,
)


def stream_platform_generation(model_id: str, request: GenerationRequest) -> Generator:
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
    response_stream = model.generate_content_stream(
        contents, generation_config=generation_config
    )
    for chunk in response_stream:
        yield chunk
