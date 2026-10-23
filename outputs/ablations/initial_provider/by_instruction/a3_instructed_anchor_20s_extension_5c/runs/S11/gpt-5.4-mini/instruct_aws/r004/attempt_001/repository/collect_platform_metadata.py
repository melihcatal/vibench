from typing import Any, Dict

from model_client import invoke_bedrock_model, load_platform_config
from model_models import PlatformRequest, normalize_request, wrap_response


def collect_platform_metadata(prompt: str) -> Dict[str, Any]:
    config = load_platform_config()
    request = PlatformRequest(prompt=prompt, model_id=config.model_id)
    response = invoke_bedrock_model(normalize_request(request), model_id=request.model_id)
    wrapped = wrap_response(response)
    return {"text": wrapped.text, "usage": wrapped.usage, "resource_id": wrapped.resource_id, "model_id": wrapped.model_id, "raw": wrapped.raw}
