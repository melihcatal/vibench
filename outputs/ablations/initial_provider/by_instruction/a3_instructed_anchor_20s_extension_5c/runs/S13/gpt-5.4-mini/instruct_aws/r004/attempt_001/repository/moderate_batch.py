import json

from safety_client import invoke_bedrock_json, AWS_BEDROCK_MODEL_ID
from safety_models import build_batch_payload


def moderate_batch(messages):
    prompt = {
        "modelId": AWS_BEDROCK_MODEL_ID,
        "input": build_batch_payload(messages),
        "task": "moderate_batch",
    }
    return invoke_bedrock_json(json.dumps(prompt))
