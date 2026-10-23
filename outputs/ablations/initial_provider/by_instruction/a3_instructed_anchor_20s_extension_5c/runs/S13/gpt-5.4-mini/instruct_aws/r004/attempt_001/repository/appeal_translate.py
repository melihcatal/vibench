import json

from safety_client import invoke_bedrock_json, AWS_BEDROCK_MODEL_ID


def appeal_translate(text, target_language):
    prompt = {
        "modelId": AWS_BEDROCK_MODEL_ID,
        "input": {"text": text, "target_language": target_language},
        "task": "appeal_translate",
    }
    return invoke_bedrock_json(json.dumps(prompt))
