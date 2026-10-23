from google.cloud import aiplatform
from typing import List, Dict, Any, AsyncIterable


def embed_caption_chunk(text: str) -> List[float]:
    client = aiplatform.gapic.PredictionServiceClient(
        client_options={"api_endpoint": "us-central1-aiplatform.googleapis.com"}
    )
    endpoint = f"projects/{client.project}/locations/us-central1/publishers/google/models/textembedding-gecko@001"

    instance = {"content": text}
    instances = [instance]
    response = client.predict(endpoint=endpoint, instances=instances)
    return response.predictions[0]["embeddings"]["values"]


def caption_embedding(
    transcript_stream: AsyncIterable[Dict[str, Any]],
) -> AsyncIterable[Dict[str, Any]]:
    async for result in transcript_stream:
        if result["is_final"]:
            embedding = embed_caption_chunk(result["transcript"])
            yield {
                **result,
                "embedding": embedding,
            }
        else:
            yield result
