import boto3

bedrock_runtime = boto3.client("bedrock-runtime", region_name="us-west-2")


def embed_text(text):
    response = bedrock_runtime.invoke_model(
        ModelId="amazon.titan-embed-text-v1", Body=json.dumps({"inputText": text})
    )
    return json.loads(response["Body"].read())["embedding"]
