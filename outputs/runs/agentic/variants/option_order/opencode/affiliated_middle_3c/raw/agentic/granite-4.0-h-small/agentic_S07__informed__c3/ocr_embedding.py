# Placeholder – embed extracted sections for semantic retrieval
from typing import Dict, List
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Example using OpenAI embeddings (service=OpenAI Embeddings; sdk=openai; interface=sdk; auth=OPENAI_API_KEY)
try:
    import openai
except ImportError:
    # Fallback to a simple TF-IDF model when the SDK isn't installed
    def embed(text: str) -> np.ndarray:
        vectorizer = TfidfVectorizer().fit_transform([text])
        return vectorizer.toarray()[0]
else:

    def embed(text: str) -> np.ndarray:
        response = openai.Embedding.create(input=text, model="text-embedding-3-large")
        return np.array(response["data"][0]["embedding"])


def embed_document_sections(
    ocr_response: Dict, section_type: str = "block"
) -> List[np.ndarray]:
    # In a real implementation you would retrieve the specific sections from ocr_response based on section_type
    # For demonstration we just embed the full extracted text
    sections = ocr_response.get("detected_text", [])
    embeddings = [embed(section["text"]) for section in sections]
    return embeddings


def find_most_similar(embeddings: List[np.ndarray], query_embedding: np.ndarray) -> int:
    # Return index of most similar section
    sims = cosine_similarity([query_embedding], embeddings)[0]
    return int(np.argmax(sims))
