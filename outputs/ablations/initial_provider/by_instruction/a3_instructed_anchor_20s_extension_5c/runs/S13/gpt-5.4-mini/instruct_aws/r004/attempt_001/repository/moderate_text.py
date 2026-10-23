import json

from safety_client import invoke_bedrock_json, AWS_BEDROCK_MODEL_ID
from safety_models import build_message_payload


def moderate_text(text, metadata=None):
    payload = build_message_payload(text, metadata)
    prompt = {
        "modelId": AWS_BEDROCK_MODEL_ID,
        "input": payload,
        "task": "moderate_text",
    }
    response = invoke_bedrock_json(json.dumps(prompt))
    return response


def main(text, metadata=None):
    return moderate_text(text, metadata)
