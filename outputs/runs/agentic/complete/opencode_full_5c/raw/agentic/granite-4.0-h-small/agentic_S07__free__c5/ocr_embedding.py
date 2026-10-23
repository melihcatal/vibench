import os
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from document_client import TextractClient
from extract_layout import extract_layout_from_image

# -------------------------------------------------
# LATER-STEP: ocr_embedding.py
# Embed extracted document sections for semantic retrieval using SentenceTransformers
# -------------------------------------------------

# Load a small, fast model (e.g., all-MiniLM-L6-v2) – already installed via pip
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
model = SentenceTransformer(MODEL_NAME, device="cpu")

# Index example: create a simple FAISS index for demo purposes
index = faiss.IndexFlatL2(384)  # 384 = embedding dimension for MiniLM-L6-v2

# ------------------------------------------------------------------
# Helper functions
# ------------------------------------------------------------------

def embed_document_sections(image_path: str) -> dict:
    """Extract layout blocks and embed each block (e.g., paragraph, table cell).",
    Returns a dict mapping a block ID to its embedding vector.
    """
    raw_bytes = open(image_path, "rb").read()
    layout = TextractClient().extract_layout(raw_bytes)
    embeddings = {}
    for block in layout.get("Blocks", []):
        if block.get("BlockType") not in ("LINE", "CELL", "WORD"):
            continue  # skip non-text blocks
        text = block.get("Text", "")
        tokens = model.encode(text, convert_to_tensor=True).cpu().numpy().flatten()
        # Insert into FAISS index (demo: just store)
        vectors = np.array([tokens], dtype=np.float32)
        index.add(vectors)
        embeddings[block.get("Id", "")] = tokens.tolist()
    return embeddings

# ------------------------------------------------------------------
# Simple semantic search demo
# ------------------------------------------------------------------
def semantic_search(query: str, embeddings: dict, top_k: int = 5):
    """Return the top_k most similar block texts to a query string.","
    query_vec = model.encode(query, convert_to_tensor=True).cpu().numpy().flatten()
    D, I = index.search(np.array([query_vec], dtype=np.float32), top_k)
    results = []
    for dist, idx in zip(D[0], I[0]):
        text = next((b["Text"] for b in extract_layout_from_image(os.path.abspath(image_path)) if b.get("Id") == str(idx)), "<unknown>")
        results.append({"text": text, "score": 1 - (dist / np.linalg.norm(query_vec))})
    return results

# ------------------------------------------------------------------
# Example usage (uncomment to run)
# ------------------------------------------------------------------
# img = "sample_invoice.png"
# idx = embed_document_sections(img)
# hits = semantic_search("total due date", idx)
# print(hits)
