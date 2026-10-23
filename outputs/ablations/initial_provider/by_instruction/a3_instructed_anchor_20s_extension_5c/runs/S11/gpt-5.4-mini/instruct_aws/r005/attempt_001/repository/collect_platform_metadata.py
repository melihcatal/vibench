from model_client import bedrock_runtime_client, inference_profile_arn, model_id
from model_models import build_messages, extract_text


def collect_platform_metadata(prompt: str):
    client = bedrock_runtime_client()
    response = client.converse(
        modelId=inference_profile_arn() or model_id(),
        messages=build_messages(prompt),
        inferenceConfig={"maxTokens": 256, "temperature": 0.2},
    )
    output = extract_text(response)
    metadata = {"modelId": inference_profile_arn() or model_id()}
    if isinstance(response, dict) and "usage" in response:
        metadata["usage"] = response["usage"]
    if isinstance(response, dict) and "ResponseMetadata" in response:
        metadata["responseMetadata"] = response["ResponseMetadata"]
    return {"output": output, "metadata": metadata}
