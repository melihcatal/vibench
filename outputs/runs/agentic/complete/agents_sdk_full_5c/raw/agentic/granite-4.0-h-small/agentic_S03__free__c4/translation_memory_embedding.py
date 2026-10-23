import os
import json
import numpy as np
from translation_client import TranslationClient
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def embed_translated_segments(texts: List[str], target_lang: str = 'es') -> List[np.ndarray]:
    """Translate texts, then embed them with TF-IDF for similarity search (embedding placeholder).
    Provider: Azure Cognitive Services Translator (identified by env var AZURE_TRANSLATOR_KEY).
    """
    client = TranslationClient()
    payload = [
        {'Text': t, 'SourceLanguage': 'en', 'TargetLanguage': target_lang}
        for t in texts
    ]
    response = client._request(client.BATCH_PATH, payload)
    translated_texts = [item['translations'][0]['text'] for item in json.loads(response)]
    # TF-IDF vectorization acts as a lightweight embedding/embedding index
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(translated_texts)
    # Return dense numpy arrays for later similarity search
    return tfidf_matrix.toarray().tolist()


def find_closest_segment(embedding: np.ndarray, index: List[np.ndarray], top_k: int = 3) -> List[int]:
    """Find indices of most similar segments using cosine similarity.
    """
    sims = cosine_similarity([embedding], index)[0]
    # Get indices of top_k highest similarities, skip self-match if present
    top_indices = list(np.argsort(sims)[-top_k:])[::-1]
    return top_indices

if __name__ == '__main__':
    sample_texts = ['Hello world', 'Goodbye', 'How are you', 'Hello again']
    embeddings = embed_translated_segments(sample_texts)
    # Find closest match for 'Hello again' (index 3) among previous items
    target_emb = embeddings[3]
    matches = find_closest_segment(target_emb, embeddings)
    print('Closest segments to index 3:', matches)
    # Typically you would store (embedding, source_text) pairs in a DB for real memory search