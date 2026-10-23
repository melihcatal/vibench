import boto3

bedrock = boto3.client("bedrock-runtime", region_name="us-west-2")


def crypto_audit_embedding(text):
    model_id = "amazon.titan-embed-text-v1"
    body = {"inputText": text}
    response = bedrock.invoke_model(
        body=json.dumps(body),
        modelId=model_id,
        accept="application/json",
        contentType="application/json",
    )
    result = json.loads(response.get("body").read())
    return result["embedding"]
