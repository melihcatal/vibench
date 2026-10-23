import os

from openai import OpenAI

from storage_client import get_blob_service_client, load_config, normalize_blob_name


def stored_asset_summary(blob_name: str, container: str = None) -> str:
    config = load_config(container)
    client = get_blob_service_client(config)
    text = client.get_blob_client(container=config.container, blob=normalize_blob_name(blob_name)).download_blob().content_as_text()
    oai = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    response = oai.responses.create(model="gpt-5.4-mini", input=f"Summarize the following asset:\n{text}")
    return response.output_text
