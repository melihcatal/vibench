from google.cloud import aiplatform

from storage_client import get_blob_client


def asset_metadata_embedding(payload, config=None):
    config = config or {}
    blob = get_blob_client(config, payload["object_name"])
    metadata = {"object_name": blob.name, "content_type": blob.content_type, "size": blob.size}
    text = blob.download_as_text() if payload.get("include_text", True) else ""
    instance = {"content": f'{metadata["object_name"]}\n{metadata.get("content_type", "")}\n{text}'}
    endpoint = aiplatform.Endpoint(endpoint_name=payload["endpoint_name"])
    prediction = endpoint.predict(instances=[instance])
    return {"embedding": prediction.predictions[0], "metadata": metadata}
