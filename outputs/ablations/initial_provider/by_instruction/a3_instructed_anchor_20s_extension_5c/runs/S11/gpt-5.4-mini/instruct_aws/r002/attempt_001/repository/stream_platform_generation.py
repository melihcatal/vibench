from model_client import bedrock_runtime_client, default_model_id
from select_platform_resource import select_platform_resource


def stream_platform_generation(prompt, model_id=None):
    runtime = bedrock_runtime_client()
    resolved = select_platform_resource(model_id or default_model_id())
    target = resolved.get("inference_profile_arn") or resolved.get("model_id")
    return runtime.converse_stream(
        modelId=target,
        messages=[{"role": "user", "content": [{"text": prompt}]}],
        inferenceConfig={"maxTokens": 512, "temperature": 0.2},
    )
