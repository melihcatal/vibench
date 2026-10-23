import json
from typing import Optional

from model_client import bedrock_client, get_model_config
from model_models import JsonRequest, parse_json_output, normalize_text_output


def extract_json(text: str, schema_hint: Optional[str] = None, model_id: Optional[str] = None):
    config = get_model_config(model_id)
    client = bedrock_client(config.region_name)
    request = JsonRequest(text=text, schema_hint=schema_hint)
    prompt = f"Extract structured JSON from the text. Return only valid JSON.\n\nText:\n{request.text}"
    if request.schema_hint:
        prompt += f"\n\nSchema hint:\n{request.schema_hint}"
    payload = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": config.max_tokens,
        "temperature": 0,
        "top_p": config.top_p,
        "messages": [{"role": "user", "content": [{"type": "text", "text": prompt}]}],
    }
    response = client.invoke_model(modelId=config.model_id, body=json.dumps(payload))
    body = json.loads(response["body"].read())
    return parse_json_output(normalize_text_output(body))
