import os
from typing import List
from sentence_transformers import SentenceTransformer
from document_models import LayoutBlock

def embed_document_sections(blocks: List[LayoutBlock]) -> List[List[float]]:
    """Embed extracted document sections for semantic retrieval using Sentence Transformers."""
    model = SentenceTransformer('all-MiniLM-L6-v2')
    texts = [block.text for block in blocks]
    embeddings = model.encode(texts, convert_to_tensor=False)
    
    return embeddings.tolist()