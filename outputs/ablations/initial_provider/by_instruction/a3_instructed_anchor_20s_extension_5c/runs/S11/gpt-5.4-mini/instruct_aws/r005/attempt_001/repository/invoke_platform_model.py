from model_client import bedrock_runtime_client, inference_profile_arn, model_id
from model_models import build_messages, extract_text


def invoke_platform_model(prompt: str):
    client = bedrock_runtime_client()
    kwargs = {
        "modelId": inference_profile_arn() or model_id(),
        "messages": build_messages(prompt),
        "inferenceConfig": {"maxTokens": 256, "temperature": 0.2},
    }
    response = client.converse(**kwargs)
    return extract_text(response)
