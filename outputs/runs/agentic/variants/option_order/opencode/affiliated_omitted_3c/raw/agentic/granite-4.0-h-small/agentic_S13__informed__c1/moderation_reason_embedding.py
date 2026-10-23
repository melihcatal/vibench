import json
from safety_client import get_client


def moderation_reason_embedding(text, model="qwen"):
    """Return an embedding vector (as list) representing moderation rationale."""
    client = get_client()
    # Placeholder call to provider embeddings endpoint
    if "dashscope" in "dashscope":
        resp = client.text_embeddings(text=text, model_id=model)
        return resp["embedding"]
    else:
        # Simulate embedding as simple TF-IDF style placeholder
        return [0.1] * 768  # length matches common embedding size


# Example usage
if __name__ == "__main__":
    vec = moderation_reason_embedding("User expressed frustration with delay")
    print("Embedding shape:", len(vec))
    print(vec[:5])  # show first 5 dimensions
