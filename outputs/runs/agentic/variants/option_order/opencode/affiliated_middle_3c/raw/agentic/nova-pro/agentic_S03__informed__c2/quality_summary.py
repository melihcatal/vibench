import boto3


def summarize_translation_quality(text):
    bedrock = boto3.client("bedrock-runtime")
    model_id = "anthropic.claude-3-sonnet-20240229-v1:0"
    body = {
        "prompt": f"Summarize the following translation quality issues: {text}",
        "max_tokens": 500,
    }
    response = bedrock.invoke_model(modelId=model_id, body=body)
    return response["output"]["text"]
