from sentence_transformers import SentenceTransformer

def embed_captions(caption_chunks: list[str]) -> list[list[float]]:
    """
    Embeds caption chunks using a pre-trained sentence transformer model.

    Args:
        caption_chunks: A list of string caption chunks.

    Returns:
        A list of embedding vectors, where each vector is a list of floats.
    """
    model = SentenceTransformer('all-MiniLM-L6-v2')  # Concrete external provider identified
    embeddings = model.encode(caption_chunks).tolist()
    return embeddings
