import os
from typing import Optional

import openai

from storage_client import StorageClient
from storage_models import ObjectMetadata


class OpenAIEmbedder:
    def __init__(self):
        self.api_key = os.environ.get("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError(
                "OPENAI_API_KEY environment variable is required for OpenAI embeddings"
            )
        self.model = os.environ.get("OPENAI_EMBEDDING_MODEL", "text-embedding-3-large")
        self.dimensions = int(os.environ.get("OPENAI_EMBEDDING_DIMENSIONS", "1024"))
        self._client = None

    @property
    def client(self) -> openai.OpenAI:
        if self._client is None:
            self._client = openai.OpenAI(api_key=self.api_key)
        return self._client

    def embed_text(
        self,
        text: str,
        model: Optional[str] = None,
        dimensions: Optional[int] = None,
    ) -> dict:
        target_model = model or self.model
        target_dimensions = dimensions or self.dimensions

        kwargs = {
            "input": text,
            "model": target_model,
        }
        if target_dimensions and "text-embedding-3" in target_model:
            kwargs["dimensions"] = target_dimensions

        response = self.client.embeddings.create(**kwargs)

        embedding = response.data[0].embedding

        return {
            "embedding": embedding,
            "model": target_model,
            "dimensions": len(embedding),
            "usage": {
                "prompt_tokens": response.usage.prompt_tokens,
                "total_tokens": response.usage.total_tokens,
            },
        }

    def embed_texts_batch(
        self,
        texts: list[str],
        model: Optional[str] = None,
        dimensions: Optional[int] = None,
    ) -> dict:
        target_model = model or self.model
        target_dimensions = dimensions or self.dimensions

        kwargs = {
            "input": texts,
            "model": target_model,
        }
        if target_dimensions and "text-embedding-3" in target_model:
            kwargs["dimensions"] = target_dimensions

        response = self.client.embeddings.create(**kwargs)

        embeddings = [item.embedding for item in response.data]

        return {
            "embeddings": embeddings,
            "model": target_model,
            "dimensions": len(embeddings[0]) if embeddings else 0,
            "count": len(embeddings),
            "usage": {
                "prompt_tokens": response.usage.prompt_tokens,
                "total_tokens": response.usage.total_tokens,
            },
        }


def embed_asset_metadata_and_text(
    bucket: Optional[str] = None,
    key: Optional[str] = None,
    metadata: Optional[ObjectMetadata] = None,
    extracted_text: Optional[str] = None,
    model: Optional[str] = None,
    dimensions: Optional[int] = None,
) -> dict:
    storage_client = StorageClient()
    target_bucket = bucket or storage_client.default_bucket
    if not target_bucket:
        raise ValueError("No bucket specified and S3_DEFAULT_BUCKET not set")

    if metadata is None:
        from object_metadata import get_object_metadata

        metadata = get_object_metadata(bucket=target_bucket, key=key)

    if extracted_text is None and key:
        response = storage_client.s3_client.get_object(
            Bucket=target_bucket,
            Key=key,
        )
        content = response["Body"].read()
        try:
            extracted_text = content.decode("utf-8")
        except UnicodeDecodeError:
            extracted_text = content.decode("latin-1")

    metadata_fields = {
        "bucket": metadata.bucket,
        "key": metadata.key,
        "content_type": metadata.content_type,
        "content_length": metadata.content_length,
        "storage_class": metadata.storage_class,
        "last_modified": str(metadata.last_modified)
        if metadata.last_modified
        else None,
        "custom_metadata": metadata.metadata,
    }

    metadata_string = "; ".join(
        f"{k}={v}" for k, v in metadata_fields.items() if v is not None
    )

    embedder = OpenAIEmbedder()

    metadata_embedding = embedder.embed_text(
        text=metadata_string,
        model=model,
        dimensions=dimensions,
    )

    text_embedding = None
    if extracted_text:
        chunk_size = 8000
        text_chunks = [
            extracted_text[i : i + chunk_size]
            for i in range(0, len(extracted_text), chunk_size)
        ]

        if len(text_chunks) == 1:
            text_embedding = embedder.embed_text(
                text=extracted_text,
                model=model,
                dimensions=dimensions,
            )
        else:
            text_embedding = embedder.embed_texts_batch(
                texts=text_chunks,
                model=model,
                dimensions=dimensions,
            )

    combined_input = (
        f"{metadata_string}\n\n{extracted_text}" if extracted_text else metadata_string
    )
    combined_embedding = embedder.embed_text(
        text=combined_input,
        model=model,
        dimensions=dimensions,
    )

    result = {
        "bucket": metadata.bucket,
        "key": metadata.key,
        "metadata_embedding": metadata_embedding,
        "text_embedding": text_embedding,
        "combined_embedding": combined_embedding,
        "metadata_fields": metadata_fields,
        "text_length": len(extracted_text) if extracted_text else 0,
    }

    return result


def embed_searchable_vector(
    bucket: Optional[str] = None,
    key: Optional[str] = None,
    extracted_text: Optional[str] = None,
    model: Optional[str] = None,
    dimensions: Optional[int] = None,
) -> dict:
    storage_client = StorageClient()
    target_bucket = bucket or storage_client.default_bucket
    if not target_bucket:
        raise ValueError("No bucket specified and S3_DEFAULT_BUCKET not set")

    if extracted_text is None and key:
        response = storage_client.s3_client.get_object(
            Bucket=target_bucket,
            Key=key,
        )
        content = response["Body"].read()
        try:
            extracted_text = content.decode("utf-8")
        except UnicodeDecodeError:
            extracted_text = content.decode("latin-1")

    embedder = OpenAIEmbedder()

    embedding_result = embedder.embed_text(
        text=extracted_text,
        model=model,
        dimensions=dimensions,
    )

    return {
        "bucket": target_bucket,
        "key": key,
        "embedding": embedding_result["embedding"],
        "model": embedding_result["model"],
        "dimensions": embedding_result["dimensions"],
        "text_length": len(extracted_text),
        "usage": embedding_result["usage"],
    }
