import json

from safety_client import invoke_bedrock_json, AWS_BEDROCK_MODEL_ID


def moderation_summary(decisions):
    prompt = {"modelId": AWS_BEDROCK_MODEL_ID, "input": {"decisions": decisions}, "task": "moderation_summary"}
    return invoke_bedrock_json(json.dumps(prompt))
