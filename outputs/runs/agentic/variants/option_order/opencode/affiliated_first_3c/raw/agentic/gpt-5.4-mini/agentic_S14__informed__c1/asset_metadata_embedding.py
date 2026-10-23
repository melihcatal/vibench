from typing import Dict, List, Optional

from openai import OpenAI


def asset_metadata_embedding(metadata: Dict[str, object], extracted_text: str, model: str = 'text-embedding-3-small', api_key: Optional[str] = None) -> List[float]:
    client = OpenAI(api_key=api_key)
    payload = '
'.join(f'{k}: {v}' for k, v in sorted(metadata.items())) + '
' + extracted_text
    response = client.embeddings.create(model=model, input=payload)
    return response.data[0].embedding
