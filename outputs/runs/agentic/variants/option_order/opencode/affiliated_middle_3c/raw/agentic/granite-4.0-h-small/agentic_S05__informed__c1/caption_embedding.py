import asyncio
import json
import os
import numpy as np
from sentence_transformers import SentenceTransformer
from speech_client import get_client
from speech_models import normalize_transcript

# -------------------------------
# Embedding integration with Sentence Transformers (local) or via hosted model API
# -------------------------------

# Choose a model identifier (example uses a local model - change to hosted if needed)
MODEL_ID = "all-MiniLM-L6-v2"  # local; hosted versions: openai, google, etc.
model = SentenceTransformer(MODEL_ID)


def embed_text(text: str) -> np.ndarray:
    """Return a numpy vector embedding for input text."""
    return model.encode(text, convert_to_numpy=True)


async def build_caption_embeddings():
    # Placeholder async audio source that yields interim results
    async def microphone_chunks():
        for i in range(4):
            # Suppose each chunk is already a transcript fragment
            yield {
                "transcript": f"Chunk {i}: Let's discuss the roadmap.",
                "confidence": 0.9,
                "is_final": False,
            }
            await asyncio.sleep(0.5)
        # Final consolidated transcript
        yield {
            "transcript": "Final transcript: Discuss roadmap and assign tasks.",
            "confidence": 0.96,
            "is_final": True,
        }

    client = get_client()  # Not used directly here; placeholder for real stream
    listen_cfg = {"language": "en-US", "punctuation": True}
    source = client.listen(source=microphone_chunks(), **listen_cfg)

    embeddings = []
    async for result in source.listen():
        if result.get("is_final"):
            norm = normalize_transcript(result)
            vec = embed_text(norm["transcript"])
            embeddings.append(vec)
    # Store or forward embeddings for semantic search (here just print)
    print(
        json.dumps(
            {
                "embeddings_count": len(embeddings),
                "first_vec": embeddings[0].tolist() if embeddings else [],
            }
        )
    )


if __name__ == "__main__":
    asyncio.run(build_caption_embeddings())
