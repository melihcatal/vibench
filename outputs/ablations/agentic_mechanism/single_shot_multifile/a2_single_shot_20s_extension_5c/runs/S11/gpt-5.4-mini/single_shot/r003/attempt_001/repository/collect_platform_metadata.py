from typing import Any, Dict, Optional

from model_client import get_client, resolve_model_name
from model_models import PlatformMetadataResult, normalize_text


def collect_platform_metadata(prompt: str, model: Optional[str] = None) -> PlatformMetadataResult:
    client = get_client()
    model_name = resolve_model_name(model)
    response = client.responses.create(
        model=model_name,
        input=normalize_text(prompt),
        max_output_tokens=256,
    )
    text = getattr(response, "output_text", "") or ""
    usage = getattr(response, "usage", None)
    usage_data: Dict[str, Any] = {}
    if usage is not None:
        usage_data = {
            "input_tokens": getattr(usage, "input_tokens", None),
            "output_tokens": getattr(usage, "output_tokens", None),
            "total_tokens": getattr(usage, "total_tokens", None),
        }
    return PlatformMetadataResult(text=text, model=model_name, resource_id=getattr(response, "model", model_name), usage=usage_data, raw_response=response)
