from typing import Optional

from cohere import Client


def embed_asset_metadata(metadata_text: str, extracted_text: str, model: str = 'embed-english-v3.0') -> dict:
    client = Client()
    texts = [metadata_text, extracted_text]
    response = client.embed(texts=texts, model=model, input_type='search_document')
    return {'model': model, 'embeddings': response.embeddings, 'texts': texts}
