import boto3


def embed_log_message(text):
    client = boto3.client("bedrock-runtime", region_name="us-west-2")
    response = client.invoke_model(
        ModelId="amazon.titan-embed-text-v1",
        ContentType="application/json",
        Body=json.dumps({"inputText": text}),
    )
    return json.loads(response["Body"].read())["embedding"]
