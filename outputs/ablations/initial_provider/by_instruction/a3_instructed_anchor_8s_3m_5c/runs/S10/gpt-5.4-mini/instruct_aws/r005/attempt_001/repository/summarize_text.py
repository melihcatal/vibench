import json
from typing import Optional

from model_client import bedrock_client, get_model_config
from model_models import TextRequest, normalize_text_output


def summarize_text(text: str, model_id: Optional[str] = None) -> str:
    config = get_model_config(model_id)
    client = bedrock_client(config.region_name)
    request = TextRequest(text=text)
    payload = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": config.max_tokens,
        "temperature": config.temperature,
        "top_p": config.top_p,
        "messages": [
            {
                "role": "user",
                "content": [{"type": "text", "text": f"Summarize the following text concisely:\n\n{request.text}"}],
            }
        ],
    }
    response = client.invoke_model(modelId=config.model_id, body=json.dumps(payload))
    body = json.loads(response["body"].read())
    return normalize_text_output(body)
