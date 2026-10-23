import boto3

TITAN_EMBEDDINGS_CLIENT = boto3.client("bedrock-runtime")


def embed_transcript(transcript):
    model_id = "amazon.titan-embed-text-v1"
    body = {"inputText": transcript}
    response = TITAN_EMBEDDINGS_CLIENT.invoke_model(
        body=json.dumps(body),
        modelId=model_id,
        accept="application/json",
        contentType="application/json",
    )
    result = json.loads(response.get("body").read())
    return result["embedding"]
