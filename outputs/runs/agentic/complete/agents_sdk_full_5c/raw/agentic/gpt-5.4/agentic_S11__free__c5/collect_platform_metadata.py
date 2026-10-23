from __future__ import annotations

from typing import Any, Dict, Optional

from vertexai.generative_models import GenerationConfig

from model_client import get_model
from model_models import PlatformRequest, candidate_text, extract_usage_metadata



def collect_platform_metadata(
    prompt: str,
    model_name: Optional[str] = None,
    system_instruction: Optional[str] = None,
) -> Dict[str, Any]:
    request = PlatformRequest(prompt=prompt, system=system_instruction)
    model = get_model(model_name=model_name)
    response = model.generate_content(
        request.to_messages(),
        generation_config=GenerationConfig(
            temperature=request.temperature,
            max_output_tokens=request.max_tokens,
        ),
    )
    first_candidate = response.candidates[0] if getattr(response, "candidates", None) else None
    return {
        "text": response.text,
        "model": model_name or "gemini-1.5-pro",
        "usage": extract_usage_metadata(response),
        "resource": getattr(response, "model_version", None),
        "candidate_text": candidate_text(first_candidate) if first_candidate is not None else response.text,
        "response_id": getattr(response, "response_id", None),
    }
