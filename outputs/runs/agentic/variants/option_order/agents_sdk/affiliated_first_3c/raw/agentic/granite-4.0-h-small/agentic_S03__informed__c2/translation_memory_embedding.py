import os
import numpy as np
from google.cloud import translate_v2 as translate
from ibm_watsonx_ai.api import EmbeddingsServiceClient
from ibm_watsonx_ai.api.api_credentials import APICredential

# Watsonx credentials (environment variables)
WATSONX_API_KEY = os.getenv('WATSONX_API_KEY')
WATSONX_PROJECT_ID = os.getenv('WATSONX_PROJECT_ID')
if not WATSONX_API_KEY or not WATSONX_PROJECT_ID:
    raise RuntimeError('Set WATSONX_API_KEY and WATSONX_PROJECT_ID environment variables')

credential = APICredential(api_key=WATSONX_API_KEY)
client = EmbeddingsServiceClient(credential=credential)

TRANSLATE = translate.Client()

def embed_translated_segments(texts, target_lang='es'):
    """Translate texts and embed each segment with IBM Slate embeddings.
    Returns list of numpy arrays representing embeddings.
    """
    translated = [TRANSLATE.translate(t, target_language=target_lang)['translatedText'] for t in texts]
    vectors = []
    for txt in translated:
        resp = client.create_embeddings(model_id='slate.125m.en', input=[txt])
        vec = resp.embeddings[0].vector if resp.embeddings else np.zeros(384)
        vectors.append(np.array(vec, dtype=np.float32))
    return vectors

def find_best_match(query, vectors, top_k=5):
    """Find top-k most similar embeddings using cosine similarity.
    Returns list of indices.
    """
    q_vec = client.create_embeddings(model_id='slate.125m.en', input=[query])[0].embeddings[0].vector
    q_vec = np.array(q_vec, dtype=np.float32)
    sims = []
    for i, emb in enumerate(vectors):
        sim = np.dot(q_vec, emb) / (np.linalg.norm(q_vec) * np.linalg.norm(emb) + 1e-9)
        sims.append((sim, i))
    sims.sort(reverse=True)
    return [i for _, i in sims[:top_k]]