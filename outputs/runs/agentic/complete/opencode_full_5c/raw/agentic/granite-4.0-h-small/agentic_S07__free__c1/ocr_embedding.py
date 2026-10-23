# [LATER-STEP] ocr_embedding.py
"""Embed extracted document sections for semantic retrieval using Cohere embedding model"""

import os
import cohere
from typing import List, Dict, Any
from document_models import OCRResponse

# Load configuration for Cohere API key from environment (helper may be more sophisticated)
COHERE_API_KEY = os.getenv("COHERE_API_KEY")
if not COHERE_API_KEY:
    raise RuntimeError(
        "Set COHERE_API_KEY environment variable before running embedding"
    )

# Initialise Cohere client
c = cohere.Client(COHERE_API_KEY)

EMBED_MODEL = "embed-english-v3.0"  # concrete model identifier


def embed_blocks(ocr_resp: OCRResponse) -> List[Dict[str, Any]]:
    """Generate embeddings for each text block in the OCR response"""
    texts = [
        block["Text"] for block in ocr_resp.blocks if block.get("Confidence", 0) > 70
    ]
    # Cohere embed accepts a list of strings; returns a list of embedding vectors
    response = c.embed(model=EMBED_MODEL, texts=texts)
    embeddings = response.embeddings
    # Pair each embedding with its block metadata for downstream use
    return [
        {
            "id": i,
            "text": text,
            "embedding": emb.vector.tolist(),  # numpy array converted to list
        }
        for i, (text, emb) in enumerate(zip(texts, embeddings))
    ]


if __name__ == "__main__":
    import json, sys

    if len(sys.argv) != 2:
        print("Usage: python ocr_embedding.py <ocr-json>")
        sys.exit(1)
    with open(sys.argv[1], "r") as f:
        ocr_json = json.load(f)
    ocr_resp = OCRResponse(ocr_json)
    embeddings = embed_blocks(ocr_resp)
    print(json.dumps(embeddings, indent=2))
