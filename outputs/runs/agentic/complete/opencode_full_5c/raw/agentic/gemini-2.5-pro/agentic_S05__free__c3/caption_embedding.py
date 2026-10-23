import os
from google.cloud import aiplatform
import vertexai
from vertexai.language_models import TextEmbeddingInput, TextEmbeddingModel

PROJECT_ID = os.environ.get("GCP_PROJECT")
LOCATION = os.environ.get("GCP_REGION")


def embed_caption_chunk(caption_chunk: str):
    vertexai.init(project=PROJECT_ID, location=LOCATION)

    model = TextEmbeddingModel.from_pretrained("text-embedding-004")

    inputs = [TextEmbeddingInput(caption_chunk, "SEMANTIC_SIMILARITY")]

    embeddings = model.get_embeddings(inputs)

    return embeddings[0].values


if __name__ == "__main__":
    caption = "The next agenda item is the quarterly budget review."
    embedding = embed_caption_chunk(caption)
    print(f"Caption: {caption}")
    print(f"Embedding vector dimension: {len(embedding)}")
    print(f"First 5 dimensions: {embedding[:5]}")
