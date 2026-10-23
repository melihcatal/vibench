import json

from model_client import get_bedrock_client, get_model_id
from model_models import extract_bedrock_text, normalize_text_payload


def extract_json(payload, config=None):
    client = get_bedrock_client(config)
    prompt = "Extract structured JSON from the following text and return only valid JSON:\n\n" + normalize_text_payload(payload)
    response = client.converse(
        modelId=get_model_id(config),
        messages=[{"role": "user", "content": [{"text": prompt}]}],
    )
    text = extract_bedrock_text(response)
    return {"text": text, "json": json.loads(text)}
