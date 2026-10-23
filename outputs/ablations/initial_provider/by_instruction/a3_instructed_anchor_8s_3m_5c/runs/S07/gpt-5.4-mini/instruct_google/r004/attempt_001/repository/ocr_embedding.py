import os

from google.cloud import aiplatform


def embed_document_sections(sections):
    aiplatform.init(project=os.getenv("GOOGLE_CLOUD_PROJECT"), location=os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1"))
    return [len(section) for section in sections]
