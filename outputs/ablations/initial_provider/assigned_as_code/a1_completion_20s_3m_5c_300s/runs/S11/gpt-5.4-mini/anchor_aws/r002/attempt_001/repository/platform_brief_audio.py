import boto3


def platform_brief_audio(payload, config=None):
    config = config or {}
    client = boto3.client("bedrock-runtime", region_name=config.get("region", "us-east-1"))
    response = client.invoke_model_with_response_stream(
        modelId=config.get("audio_model_id", "amazon.nova-sonic-v1:0"),
        body=("{" + f'"inputText":"{payload["text"].replace("\\", "\\\\").replace("\"", "\\\"")}"' + "}").encode("utf-8"),
        contentType="application/json",
        accept="application/json",
    )
    return {"response": response}
