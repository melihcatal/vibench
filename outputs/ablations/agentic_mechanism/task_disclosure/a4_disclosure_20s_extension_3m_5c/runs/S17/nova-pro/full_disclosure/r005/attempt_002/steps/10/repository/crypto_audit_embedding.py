import os
import pinecone

PINECONE_API_KEY = os.getenv('PINECONE_API_KEY')

def embed_crypto_audit_notes(notes):
    pinecone.init(api_key=PINECONE_API_KEY, environment='us-west1-gcp')
    index = pinecone.Index('crypto-audit')
    vectors = []
    for note in notes:
        vector = get_embedding(note)
        vectors.append((str(uuid.uuid4()), vector, {'note': note}))
    index.upsert(vectors)
    pinecone.pod_index('crypto-audit').delete()
    pinecone.disconnect()

def get_embedding(text):
    # Placeholder for actual embedding logic
    return [0.1] * 128