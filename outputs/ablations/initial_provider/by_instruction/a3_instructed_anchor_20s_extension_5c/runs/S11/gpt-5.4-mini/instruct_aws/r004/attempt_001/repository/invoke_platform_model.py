from model_client import invoke_bedrock_model, load_platform_config
from model_models import PlatformRequest, normalize_request, wrap_response


def invoke_platform_model(prompt: str):
    config = load_platform_config()
    request = PlatformRequest(prompt=prompt, model_id=config.model_id)
    response = invoke_bedrock_model(normalize_request(request), model_id=request.model_id)
    return wrap_response(response)
