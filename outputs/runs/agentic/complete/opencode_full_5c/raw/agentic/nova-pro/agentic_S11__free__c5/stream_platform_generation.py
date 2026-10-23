import boto3

bedrock_client = boto3.client("bedrock-runtime")


def stream_generation(model_id, prompt):
    response = bedrock_client.invoke_model(
        modelId=model_id, body={"prompt": prompt, "max_tokens": 50}
    )
    return response
