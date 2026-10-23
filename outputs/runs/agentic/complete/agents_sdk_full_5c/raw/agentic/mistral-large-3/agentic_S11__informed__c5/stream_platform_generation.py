from typing import Iterator
import vertexai
from vertexai.generative_models import GenerativeModel
from model_client import get_platform_config
from model_models import PlatformRequest, PlatformStreamChunk

def stream_platform_generation(request: PlatformRequest) -> Iterator[PlatformStreamChunk]:
    config = get_platform_config()
    vertexai.init(project=config["project_id"], location=config["location"])
    model = GenerativeModel(model_name="gemini-1.5-pro-001")
    
    responses = model.generate_content(
        contents=request.prompt,
        generation_config={
            "max_output_tokens": request.max_tokens,
            "temperature": request.temperature,
        },
        stream=True,
    )
    
    for response in responses:
        yield PlatformStreamChunk(
            chunk=response.text,
            metadata={
                "model_id": "gemini-1.5-pro-001",
                "chunk_id": response._chunk_id,
            }
        )