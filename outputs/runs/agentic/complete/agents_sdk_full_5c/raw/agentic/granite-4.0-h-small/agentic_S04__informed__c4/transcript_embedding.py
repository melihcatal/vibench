import os
from speech_models import TranscriptionResult
from sentence_transformers import SentenceTransformer

# Expected environment variables: COHERE_API_KEY (or any embedding provider)

def transcript_embedding(transcript_text: str):
    """Embed transcript segments using Cohere Embed API for semantic retrieval.
    Returns list of embedding vectors (numpy arrays).
    """
    import numpy as np
    from cohere import Cohere
    co = Cohere(os.getenv('COHERE_API_KEY'))
    # Cohere's embed endpoint returns embeddings for each text passed; we embed the whole transcript
    response = co.embed(texts=[transcript_text])
    embeddings = response.embeddings[0].embedding  # list of floats
    vec = np.array(embeddings)
    print(f'Embedding shape: {vec.shape}')
    return vec

if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print('Usage: transcript_embedding.py <transcript_text>')
        sys.exit(1)
    text = sys.argv[1]
    vec = transcript_embedding(text)
    print('First 5 dims:', vec[:5])
