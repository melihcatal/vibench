# [LATER-STEP] transcript_embedding.py
# Embed transcript segments for semantic retrieval using Cohere Embed API

import os
import cohere

COHERE_API_KEY = os.getenv("COHERE_API_KEY")
if not COHERE_API_KEY:
    raise RuntimeError("COHERE_API_KEY environment variable not set")

client = cohere.Client(COHERE_API_KEY)

def embed_transcript(transcript: str, model: str = "embed-english-light-v3.0") -> List[List[float]]:
    """Embeds the full transcript text using Cohere's embedding model.
    Returns a list of vectors (one per sentence) for semantic retrieval.
    """
    # Split into sentences for finer granularity
    import re
    sentences = [s.strip() for s in re.split(r'(?<=[.!?]) +', transcript) if s.strip()]
    embeddings = client.embed(
        model=model,
        texts=sentences
    )
    # embeddings is a list of CohereEmbedding objects; convert to plain lists
    return [emb.embedding for emb in embeddings]

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: transcript_embedding.py <transcript_text>")
        sys.exit(1)
    transcript = sys.argv[1]
    vecs = embed_transcript(transcript)
    print(f"Generated {len(vecs)} sentence embeddings.")
    # Print first few vectors for verification
    for i, vec in enumerate(vecs[:5]):
        print(f"Sentence {i+1}: {vec[:5]}...")
