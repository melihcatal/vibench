from sentence_transformers import SentenceTransformer

def embed_script(text: str) -> list:
    """
    Embeds narration scripts for voice-asset search using Sentence Transformers.
    """
    model = SentenceTransformer("all-MiniLM-L6-v2")
    embedding = model.encode(text, convert_to_tensor=False)
    return embedding.tolist()