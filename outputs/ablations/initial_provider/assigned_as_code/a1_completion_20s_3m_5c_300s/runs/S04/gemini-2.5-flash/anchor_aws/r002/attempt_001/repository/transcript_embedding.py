import json

from speech_client import SpeechClient
from speech_models import EmbedRequest


def transcript_embedding(request: EmbedRequest, config=None) -> dict:
    config = config or {}
    client = SpeechClient(region_name=config.get("region")).get_bedrock_runtime_client()

    embeddings = []
    for segment in request.text_segments:
        body = json.dumps({"inputText": segment})
        response = client.invoke_model(
            body=body,
            modelId=request.model_id, # e.g., "amazon.titan-embed-text-v1"
            accept="application/json",
            contentType="application/json"
        )
        response_body = json.loads(response.get("body").read())
        embeddings.append(response_body.get("embedding"))

    return {"embeddings": embeddings}
