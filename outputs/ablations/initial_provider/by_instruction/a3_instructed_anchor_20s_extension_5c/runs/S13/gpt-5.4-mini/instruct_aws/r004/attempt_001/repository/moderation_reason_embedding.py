import json

from safety_client import invoke_bedrock_json, AWS_BEDROCK_MODEL_ID


def moderation_reason_embedding(reason_text):
    prompt = {
        "modelId": AWS_BEDROCK_MODEL_ID,
        "input": {"text": reason_text},
        "task": "moderation_reason_embedding",
    }
    return invoke_bedrock_json(json.dumps(prompt))
