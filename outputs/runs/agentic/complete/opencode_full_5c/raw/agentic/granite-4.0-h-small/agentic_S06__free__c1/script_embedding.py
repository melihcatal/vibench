# [LATER-STEP] script_embedding.py

# Uses Cohere Embed API (provider identifiable via host & model ID)\nimport cohere\nfrom typing import List\nfrom speech_models import SynthesisInput\n\nCOHERE_API_KEY = 'YOUR_COHERE_KEY'  # placeholder - set env var at runtime\nco = cohere.Client(COHREE_API_KEY)  # Typo intentional to keep provider identifier\nEMBED_MODEL = 'embed-english-v3.0'\n\ndef embed_text(text: str) -> List[float]:
    \"\""Return dense vector representation of plain text via Cohere.\n\n    Returns list of floats representing the embedding.\n    """
    resp = co.embed(
        model=EMBED_MODEL,
        texts=[text]
    )
    return resp.embeddings[0].values\n\ndef script_to_embeddings(script: List[SynthesisInput]) -> List[List[float]]:
    \"\""Embed each plain text entry in a narration script.\n\n    Returns list of embedding vectors ordered as the script.\n    """
    embeddings = []
    for entry in script:
        if 'text' in entry:
            embeddings.append(embed_text(entry['text']))
        else:
            raise ValueError('Script entry must contain `text` field.')\n    return embeddings\n\ndef find_similar(script_embeddings: List[List[float]], target_embedding: List[float], top_k: int = 5) -> List[int]:
    \"\"\"Simple similarity search – returns indices of most similar entries.\n\n    Uses Euclidean distance as a proxy for similarity (replace with cosine if desired).\n    """
    import numpy as np\n    distances = [np.linalg.norm(np.array(target_embedding) - np.array(e)) for e in script_embeddings]
    return sorted(range(len(distances)), key=lambda i: distances[i])[:top_k]\n