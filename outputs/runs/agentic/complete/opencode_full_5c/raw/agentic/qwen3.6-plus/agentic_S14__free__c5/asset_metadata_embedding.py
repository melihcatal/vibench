import json
from typing import Optional

from botocore.exceptions import ClientError

from storage_client import (
    get_s3_client,
    get_bedrock_runtime_client,
    handle_aws_error,
)
from storage_models import (
    StorageConfig,
    EmbeddingRequest,
    EmbeddingResponse,
    AssetMetadataEmbedRequest,
    AssetMetadataEmbedResponse,
    ObjectMetadata,
)
from object_metadata import get_object_metadata


def generate_embedding(
    text: str,
    model_id: str = "amazon.titan-embed-text-v2:0",
    dimensions: int = 1024,
    normalize: bool = True,
    config: Optional[StorageConfig] = None,
) -> EmbeddingResponse:
    bedrock_client = get_bedrock_runtime_client(config)

    body = json.dumps(
        {
            "inputText": text,
            "dimensions": dimensions,
            "normalize": normalize,
        }
    )

    try:
        response = bedrock_client.invoke_model(
            modelId=model_id,
            contentType="application/json",
            accept="application/json",
            body=body,
        )

        response_body = json.loads(response.get("body").read())

        embedding = response_body.get("embedding", [])
        input_token_count = response_body.get("inputTextTokenCount", 0)

        return EmbeddingResponse(
            success=True,
            embedding=embedding,
            model_id=model_id,
            input_token_count=input_token_count,
        )

    except ClientError as e:
        return EmbeddingResponse(
            success=False,
            model_id=model_id,
            error=handle_aws_error(e, "generate_embedding"),
        )
    except Exception as e:
        return EmbeddingResponse(
            success=False,
            model_id=model_id,
            error=f"generate_embedding error: {str(e)}",
        )


def generate_embedding_from_request(
    request: EmbeddingRequest,
    config: Optional[StorageConfig] = None,
) -> EmbeddingResponse:
    return generate_embedding(
        text=request.text,
        model_id=request.model_id,
        dimensions=request.dimensions,
        normalize=request.normalize,
        config=config,
    )


def embed_asset_metadata_and_text(
    bucket: str,
    key: str,
    extracted_text: str = "",
    model_id: str = "amazon.titan-embed-text-v2:0",
    include_metadata_fields: Optional[list] = None,
    config: Optional[StorageConfig] = None,
) -> AssetMetadataEmbedResponse:
    if include_metadata_fields is None:
        include_metadata_fields = [
            "content_type",
            "content_length",
            "last_modified",
            "storage_class",
        ]

    bedrock_client = get_bedrock_runtime_client(config)

    try:
        object_meta = get_object_metadata(bucket=bucket, key=key, config=config)

        if not object_meta.exists:
            return AssetMetadataEmbedResponse(
                success=False,
                model_id=model_id,
                error=f"Object {key} not found in bucket {bucket}",
            )

        metadata_str_parts = []
        for field_name in include_metadata_fields:
            value = getattr(object_meta, field_name, None)
            if value is not None:
                metadata_str_parts.append(f"{field_name}: {value}")

        metadata_text = "\n".join(metadata_str_parts)

        combined_text = f"Object: {key}\nBucket: {bucket}\n{metadata_text}\n\nExtracted Content:\n{extracted_text}"

        combined_body = json.dumps(
            {
                "inputText": combined_text,
                "dimensions": 1024,
                "normalize": True,
            }
        )

        metadata_only_body = json.dumps(
            {
                "inputText": metadata_text,
                "dimensions": 1024,
                "normalize": True,
            }
        )

        text_only_body = json.dumps(
            {
                "inputText": extracted_text,
                "dimensions": 1024,
                "normalize": True,
            }
        )

        combined_response = bedrock_client.invoke_model(
            modelId=model_id,
            contentType="application/json",
            accept="application/json",
            body=combined_body,
        )

        metadata_response = bedrock_client.invoke_model(
            modelId=model_id,
            contentType="application/json",
            accept="application/json",
            body=metadata_only_body,
        )

        text_response = bedrock_client.invoke_model(
            modelId=model_id,
            contentType="application/json",
            accept="application/json",
            body=text_only_body,
        )

        combined_body_parsed = json.loads(combined_response.get("body").read())
        metadata_body_parsed = json.loads(metadata_response.get("body").read())
        text_body_parsed = json.loads(text_response.get("body").read())

        return AssetMetadataEmbedResponse(
            success=True,
            combined_embedding=combined_body_parsed.get("embedding", []),
            metadata_embedding=metadata_body_parsed.get("embedding", []),
            text_embedding=text_body_parsed.get("embedding", []),
            object_metadata=object_meta,
            model_id=model_id,
        )

    except ClientError as e:
        return AssetMetadataEmbedResponse(
            success=False,
            model_id=model_id,
            error=handle_aws_error(e, "embed_asset_metadata_and_text"),
        )
    except Exception as e:
        return AssetMetadataEmbedResponse(
            success=False,
            model_id=model_id,
            error=f"embed_asset_metadata_and_text error: {str(e)}",
        )


def embed_asset_from_request(
    request: AssetMetadataEmbedRequest,
    config: Optional[StorageConfig] = None,
) -> AssetMetadataEmbedResponse:
    return embed_asset_metadata_and_text(
        bucket=request.bucket,
        key=request.key,
        extracted_text=request.extracted_text,
        model_id=request.model_id,
        include_metadata_fields=request.include_metadata_fields,
        config=config,
    )
