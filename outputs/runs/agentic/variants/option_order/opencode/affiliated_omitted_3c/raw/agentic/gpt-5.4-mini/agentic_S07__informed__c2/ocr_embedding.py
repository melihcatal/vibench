from typing import Any, Dict, List

import cohere


def embed_ocr_sections(sections: List[str], *, api_key: str, model: str = "embed-english-v3.0") -> Dict[str, Any]:
    client = cohere.Client(api_key)
    response = client.embed(texts=sections, model=model, input_type="search_document")
    return {"provider": "cohere", "embeddings": response.embeddings, "raw": response}
