import os
from google.cloud import aiplatform


def embed_crypto_audit_note(note: str) -> list[float]:
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    location = os.environ.get("VERTEX_AI_LOCATION", "us-central1")

    aiplatform.init(project=project_id, location=location)

    model = aiplatform.ai.generative_models.GenerativeModel("gemini-1.0-pro")

    response = model.generate_content(
        f"Generate a security audit summary for the following note: {note}"
    )

    embedding_model = aiplatform.ai.language_models.TextEmbeddingModel.from_pretrained(
        "textembedding-gecko@001"
    )
    embeddings = embedding_model.get_embeddings([response.text])

    return embeddings[0].values
