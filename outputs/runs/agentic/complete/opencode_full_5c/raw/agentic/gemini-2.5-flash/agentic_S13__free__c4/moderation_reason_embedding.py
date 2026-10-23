import os
from typing import List, Dict
import vertexai  # Provider identifiable import
from vertexai.preview.language_models import TextEmbeddingModel


def embed_moderation_reason(
    reason_texts: List[str], project_id: str, location: str = "us-central1"
) -> List[List[float]]:
    """Embeds moderation rationales for case retrieval using Google Cloud Vertex AI Embeddings API.

    Args:
        reason_texts: A list of moderation rationale texts to embed.
        project_id: The Google Cloud project ID.
        location: The Google Cloud location for Vertex AI.

    Returns:
        A list of embedding vectors, where each vector corresponds to a reason text.
    """
    vertexai.init(project=project_id, location=location)
    model = TextEmbeddingModel.from_pretrained(
        "text-embedding-004"
    )  # Concrete model identifier

    embeddings = []
    for text in reason_texts:
        # The API expects a list of texts for batch embedding, even for a single text.
        # The model's predict method takes a list of `TextEmbeddingInput` objects.
        # For simplicity, I'm calling predict for each text here, but for true batching,
        # you'd construct a list of inputs and call predict once.
        try:
            response = model.predict([text])
            if response.embeddings:
                embeddings.append(response.embeddings[0].values)
        except Exception as e:
            print(f"Error embedding text '{text}': {e}")
            embeddings.append([])  # Append an empty list or handle error as appropriate

    return embeddings


if __name__ == "__main__":
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT", "your-gcp-project-id")
    if project_id == "your-gcp-project-id":
        print(
            "Please set the GOOGLE_CLOUD_PROJECT environment variable or replace 'your-gcp-project-id' with your actual project ID."
        )
    else:
        reasons = [
            "The content contained hate speech directed at a protected group.",
            "The message was flagged for excessive profanity and harassment.",
            "This post violates our policy on graphic violence.",
            "The user made a legitimate appeal based on community guidelines.",
        ]

        embeddings = embed_moderation_reason(reasons, project_id)
        for i, emb in enumerate(embeddings):
            print(f"Embedding for reason {i + 1} (first 5 elements): {emb[:5]}...")
