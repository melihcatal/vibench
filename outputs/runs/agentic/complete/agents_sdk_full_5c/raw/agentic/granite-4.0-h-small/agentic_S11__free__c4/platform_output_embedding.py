# platform_output_embedding.py
# [LATER-STEP] Embed platform outputs for evaluation or retrieval

import os
from typing import Dict, Any
from sentence_transformers import SentenceTransformer

# Load a local model; path can be overridden via env var EMBEDDING_MODEL_PATH
EMBEDDING_MODEL_PATH = os.getenv('EMBEDDING_MODEL_PATH', 'all-MiniLM-L6-v2')
model = SentenceTransformer(EMBEDDING_MODEL_PATH)

def embed_output(provider_response: Dict[str, Any]) -> Dict[str, Any]:
    """Embed textual content from the provider's model response using a sentence transformer.

    Returns a dict with original response plus an 'embedding' key containing a vector (list of floats).
    """
    # Flatten all text chunks
    chunks = []
    for choice in provider_response.get('choices', []):
        delta = choice.get('delta', {})
        chunks.append(delta.get('content', ''))
    raw_text = ' '.join(chunks)
    if not raw_text.strip():
        vector = []
    else:
        vector = model.encode(raw_text, convert_to_tensor=False).tolist()
    enriched = provider_response.copy()
    enriched['embedding'] = vector
    return {'output': provider_response, 'embedding': vector}

if __name__ == '__main__':
    # Example using a dummy response
    dummy = {
        "choices": [{"delta": {"content": "The quick brown fox jumps over the lazy dog."}}]
    }
    print(embed_output(dummy))
