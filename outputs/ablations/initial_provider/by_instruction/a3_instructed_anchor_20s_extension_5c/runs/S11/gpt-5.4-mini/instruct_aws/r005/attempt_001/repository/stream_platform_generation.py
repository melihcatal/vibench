from model_client import bedrock_runtime_client, inference_profile_arn, model_id
from model_models import build_messages


def stream_platform_generation(prompt: str):
    client = bedrock_runtime_client()
    return client.converse_stream(
        modelId=inference_profile_arn() or model_id(),
        messages=build_messages(prompt),
        inferenceConfig={"maxTokens": 256, "temperature": 0.2},
    )
