import boto3

AWS_REGION = "us-west-2"

bedrock_client = boto3.client("bedrock-runtime", region_name=AWS_REGION)


def embed_text(text):
    response = bedrock_client.invoke_model(
        modelId="amazon.titan-embed-text-v1", body={"inputText": text}
    )
    return response["embedding"]
