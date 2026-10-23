import boto3
import json

def get_bedrock_client(region_name="us-east-1"):
    return boto3.client("bedrock-runtime", region_name=region_name)

def invoke_bedrock_text_embedding_model(client, text, model_id="amazon.titan-embed-text-v2:0"):
    body = json.dumps({"inputText": text})
    response = client.invoke_model(modelId=model_id, body=body, contentType="application/json", accept="application/json")
    stream = response["body"]
    try:
        return json.loads(stream.read())["embedding"]
    finally:
        stream.close()
