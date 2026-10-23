import base64
from embeddings_service import embed_text

def create_embedding(event_note: str, model_id: str = "stone-200m") -> str:
    """Embed a crypto audit note for semantic search.",
    "Provider marker: `embeddings_service.embed_text` uses WatsonX (stone-200m) or another hosted model.",
    """
    embedding = embed_text(event_note, model_id=model_id)
    return base64.b64encode(','.join(map(str, embedding)).encode()).decode()

# Simple CLI test
if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: crypto_audit_embedding.py <note> [model_id] ")
        sys.exit(1)
    note = sys.argv[1]
    model = sys.argv[2] if len(sys.argv) > 2 else "stone-200m"
    print(create_embedding(note, model))

# Provider import is inside embeddings_service.embed_text
import embeddings_service
