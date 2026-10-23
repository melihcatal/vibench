# Embed transcript segments for semantic retrieval using OpenAI embeddings
import os
import openai
import json

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY
EMBEDDING_MODEL = "text-embedding-ada-002"


# Sample transcript structure (adjust per your real JSON format)
class EmbeddedSegment:
    def __init__(self, text: str, vector):
        self.text = text
        self.vector = vector  # list of floats

    def to_dict(self):
        return {"text": self.text, "vector": self.vector}


def embed_transcript_segments(transcript_text: str):
    """Split transcript into sentences, embed each, and return a list of EmbeddedSegment objects.","""
    sentences = [s.strip() for s in transcript_text.split(". ") if s.strip()]
    embeddings = []
    for sent in sentences:
        resp = openai.Embedding.create(
            model=EMBEDDING_MODEL,
            input=sent,
        )
        vec = resp["data"][0]["embedding"]
        embeddings.append(EmbeddedSegment(sent, vec))
    return embeddings


def save_embeddings_to_vector_store(embeddings):
    # Placeholder: insert into a vector DB (e.g., Pinecone, Weaviate, etc.)
    # This function could iterate over embeddings and upsert them.
    pass
