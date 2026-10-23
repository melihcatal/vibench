from __future__ import annotations

from typing import Optional

from vertexai.generative_models import GenerationConfig

from model_client import get_model
from model_models import PlatformRequest



def invoke_platform_model(
    prompt: str,
    model_name: Optional[str] = None,
    system_instruction: Optional[str] = None,
) -> str:
    request = PlatformRequest(prompt=prompt, system=system_instruction)
    model = get_model(model_name=model_name)
    response = model.generate_content(
        request.to_messages(),
        generation_config=GenerationConfig(
            temperature=request.temperature,
            max_output_tokens=request.max_tokens,
        ),
    )
    return response.text
