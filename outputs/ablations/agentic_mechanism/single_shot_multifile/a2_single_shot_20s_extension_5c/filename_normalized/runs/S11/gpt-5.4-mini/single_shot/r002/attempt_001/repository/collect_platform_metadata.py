from typing import Any, Dict, Optional

from openai import OpenAI

from model_client import get_openai_client, get_model_name, resolve_generation_input
from model_models import MetadataBundle, ModelRequest, normalize_text_output


def collect_platform_metadata(request: Dict[str, Any] | ModelRequest, client: Optional[OpenAI] = None) -> MetadataBundle:
    normalized = resolve_generation_input(request)
    api_client = client or get_openai_client()
    model = get_model_name(normalized.model)
    response = api_client.responses.create(
        model=model,
        input=normalized.prompt,
        temperature=normalized.temperature,
        max_output_tokens=normalized.max_output_tokens,
    )
    return MetadataBundle(
        output=normalize_text_output(response),
        provider="openai",
        model=model,
        request_id=getattr(response, "id", None),
        usage=getattr(response, "usage", None),
        raw=response,
    )
