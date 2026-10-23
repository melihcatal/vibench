import json

from model_client import bedrock_runtime_client, get_config
from model_models import TextRequest, TextResponse


DEFAULT_MODEL_ID = "anthropic.claude-3-sonnet-20240229-v1:0"


def spoken_brief(request: TextRequest) -> TextResponse:
    config = get_config(DEFAULT_MODEL_ID)
    client = bedrock_runtime_client(config.region)
    prompt = f"Rewrite the following model output as a short spoken brief suitable for audio narration:\n\n{request.text}"
    payload = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": config.max_tokens,
        "temperature": config.temperature,
        "messages": [{"role": "user", "content": [{"type": "text", "text": prompt}]}],
    }
    response = client.invoke_model(modelId=config.model_id, body=json.dumps(payload))
    body = json.loads(response["body"].read())
    text = "".join(part.get("text", "") for part in body.get("content", []) if isinstance(part, dict))
    return TextResponse(text=text, raw=body)
