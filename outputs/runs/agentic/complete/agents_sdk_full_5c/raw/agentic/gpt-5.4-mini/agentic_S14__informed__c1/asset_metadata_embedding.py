from typing import Optional

from openai import OpenAI

from object_metadata import read_object_metadata
from stored_document_ocr import run_stored_document_ocr
from storage_models import EmbeddingResult, ObjectIdentifier

EMBEDDING_MODEL = "text-embedding-3-small"


def embed_asset_metadata(
    object_name: str,
    bucket_name: Optional[str] = None,
    project_id: Optional[str] = None,
    location: str = "us",
    processor_id: Optional[str] = None,
) -> EmbeddingResult:
    metadata = read_object_metadata(object_name=object_name, bucket_name=bucket_name)
    ocr_result = run_stored_document_ocr(
        object_name=object_name,
        bucket_name=bucket_name,
        project_id=project_id,
        location=location,
        processor_id=processor_id,
    )
    text = f"Object name: {metadata.object_name}\nContent type: {metadata.content_type}\nMetadata: {metadata.metadata}\nExtracted text: {ocr_result.text}"
    client = OpenAI()
    response = client.embeddings.create(model=EMBEDDING_MODEL, input=text)
    vector = response.data[0].embedding
    return EmbeddingResult(vector=vector, source_text=text, source_object=ObjectIdentifier(metadata.bucket_name, metadata.object_name))
