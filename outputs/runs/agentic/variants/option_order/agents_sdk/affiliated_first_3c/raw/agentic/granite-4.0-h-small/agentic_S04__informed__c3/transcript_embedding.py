# [LATER-STEP] transcript_embedding.py
import json
from ibm_watsonx_ai.text.embedding import EmbeddingModel
from ibm_watsonx_ai.auth import Authenticator
from ibm_watsonx_ai import Client

MODEL_ID = 'text-embedding-001'  # IBM Granite Embedding model identifier

def embed_transcript(transcript):
    # Initialize Watsonx client (provider identifiable by IBM SDK)
    authenticator = Authenticator(apikey=os.getenv('WATSONX_API_KEY'), project_id=os.getenv('WATSONX_PROJECT_ID'))
    client = Client(authenticator=authenticator)
    embedding_model = EmbeddingModel(client=client, model_id=MODEL_ID)
    doc = embedding_model.encode(text=transcript)
    # Return embedding vector and metadata
    return {
        'transcript': transcript,
        'embedding': doc.embedding.tolist(),
        'metadata': doc.metadata
    }

if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print('Usage: transcript_embedding.py <transcript_text>')
        sys.exit(1)
    text = sys.argv[1]
    embedding = embed_transcript(text)
    print(json.dumps(embedding, indent=2))
