from __future__ import annotations

from typing import Iterator, Optional

from vertexai.generative_models import GenerationConfig, GenerationResponse

from model_client import get_model
from model_models import PlatformRequest



def stream_platform_generation(
    prompt: str,
    model_name: Optional[str] = None,
    system_instruction: Optional[str] = None,
) -> Iterator[GenerationResponse]:
    request = PlatformRequest(prompt=prompt, system=system_instruction)
    model = get_model(model_name=model_name)
    stream = model.generate_content(
        request.to_messages(),
        generation_config=GenerationConfig(
            temperature=request.temperature,
            max_output_tokens=request.max_tokens,
        ),
        stream=True,
    )
    for chunk in stream:
        yield chunk
