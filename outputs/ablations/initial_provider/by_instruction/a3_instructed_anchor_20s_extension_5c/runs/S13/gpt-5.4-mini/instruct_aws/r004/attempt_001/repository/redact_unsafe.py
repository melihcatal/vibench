import json

from safety_client import invoke_bedrock_json, AWS_BEDROCK_MODEL_ID


def redact_unsafe(text):
    prompt = {"modelId": AWS_BEDROCK_MODEL_ID, "input": {"text": text}, "task": "redact_unsafe"}
    return invoke_bedrock_json(json.dumps(prompt))
