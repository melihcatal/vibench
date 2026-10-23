import boto3


def embed_translation_memory(text):
    bedrock = boto3.client("bedrock-runtime")
    model_id = "amazon.titan-embed-text-v1"
    body = {
        "inputText": text,
    }
    response = bedrock.invoke_model(modelId=model_id, body=body)
    return response["embedding"]
