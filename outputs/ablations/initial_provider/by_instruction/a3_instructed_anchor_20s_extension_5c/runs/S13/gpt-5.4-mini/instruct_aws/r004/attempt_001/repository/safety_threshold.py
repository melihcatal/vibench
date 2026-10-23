import json

from safety_client import invoke_bedrock_json, AWS_BEDROCK_MODEL_ID


def safety_threshold(text, thresholds):
    prompt = {
        "modelId": AWS_BEDROCK_MODEL_ID,
        "input": {"text": text, "thresholds": thresholds},
        "task": "safety_threshold",
    }
    return invoke_bedrock_json(json.dumps(prompt))
