from google.cloud import aiplatform
from typing import List, Dict, Any
import numpy as np
import os


async def caption_embedding(transcript_chunks: List[Dict[str, Any]]) -> Dict[str, Any]:
    aiplatform.init(project=os.getenv("GOOGLE_PROJECT_ID"), location="us-central1")

    full_transcript = " ".join(
        [chunk["transcript"] for chunk in transcript_chunks if chunk["is_final"]]
    )

    endpoint = aiplatform.Endpoint(
        endpoint_name="projects/{}/locations/us-central1/endpoints/{}".format(
            os.getenv("GOOGLE_PROJECT_ID"), os.getenv("GOOGLE_EMBEDDING_ENDPOINT_ID")
        )
    )

    instances = [{"content": full_transcript}]
    response = endpoint.predict(instances=instances)

    embeddings = response.predictions[0]["embeddings"]

    return {
        "transcript": full_transcript,
        "embedding": np.array(embeddings).tolist(),
        "dimensions": len(embeddings),
    }
