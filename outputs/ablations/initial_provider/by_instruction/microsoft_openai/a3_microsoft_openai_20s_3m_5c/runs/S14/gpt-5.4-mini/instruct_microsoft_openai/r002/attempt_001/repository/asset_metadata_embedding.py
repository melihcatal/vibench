import os

from openai import OpenAI

from storage_client import get_blob_service_client, load_config, normalize_blob_name


def asset_metadata_embedding(blob_name: str, container: str = None) -> list:
    config = load_config(container)
    client = get_blob_service_client(config)
    blob_client = client.get_blob_client(container=config.container, blob=normalize_blob_name(blob_name))
    props = blob_client.get_blob_properties()
    metadata_text = " ".join([f"{k}:{v}" for k, v in (props.metadata or {}).items()])
    extracted_text = blob_client.download_blob().content_as_text()
    oai = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    result = oai.embeddings.create(model="text-embedding-3-small", input=f"{metadata_text}\n{extracted_text}")
    return result.data[0].embedding
