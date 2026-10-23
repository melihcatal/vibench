import os
from google.cloud import kms_v1, logging_v2, dlp_v2, translate_v3
from google.cloud import aiplatform


def get_kms_client() -> kms_v1.KeyManagementServiceClient:
    """Returns a Google Cloud KMS client."""
    return kms_v1.KeyManagementServiceClient()


def get_logging_client() -> logging_v2.Client:
    """Returns a Google Cloud Logging client."""
    return logging_v2.Client()


def get_dlp_client() -> dlp_v2.DlpServiceClient:
    """Returns a Google Cloud Data Loss Prevention (DLP) client."""
    return dlp_v2.DlpServiceClient()


def get_translation_client() -> translate_v3.TranslationServiceClient:
    """Returns a Google Cloud Translation client."""
    return translate_v3.TranslationServiceClient()


def get_vertex_ai_embedding_model(project_id: str, location: str):
    """Initializes and returns a Vertex AI text embedding model."""
    aiplatform.init(project=project_id, location=location)
    # Using a common text embedding model.
    # The specific model ID might vary or evolve, "text-embedding-004" is a placeholder.
    # Always refer to the latest Vertex AI documentation for available models.
    return aiplatform.TextEmbeddingModel.from_pretrained("text-embedding-004")


if __name__ == "__main__":
    print(
        "This file provides client helper utilities for various Google Cloud Security services."
    )
    print("Example usage:")
    # kms_client = get_kms_client()
    # print(f"KMS client created: {kms_client}")
