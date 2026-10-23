import boto3


def transcript_embedding(payload, config=None):
    config = config or {}
    client = boto3.client("bedrock-runtime", region_name=config.get("region"))
    model_id = config.get("model_id") or "amazon.titan-embed-text-v1"
    segments = payload.get("segments") or []
    embeddings = []
    for segment in segments:
        text = segment.get("text") or segment.get("transcript") or ""
        if text:
            response = client.invoke_model(
                modelId=model_id,
                body=f'{{"inputText": {text!r}}}'.replace("'", '"'),
                contentType="application/json",
                accept="application/json",
            )
            embeddings.append({"text": text, "embedding": response.get("body")})
    return {"embeddings": embeddings, "model_id": model_id, "job_id": payload.get("job_id")}
