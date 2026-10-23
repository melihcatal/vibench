import json

from safety_client import invoke_bedrock_json, AWS_BEDROCK_MODEL_ID


def reviewer_brief_audio(summary_text):
    prompt = {"modelId": AWS_BEDROCK_MODEL_ID, "input": {"text": summary_text}, "task": "reviewer_brief_audio"}
    return invoke_bedrock_json(json.dumps(prompt))
