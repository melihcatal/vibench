from openai import OpenAI
import os
from typing import Dict, Any, List

def embed_asset_metadata_and_text(
    metadata: Dict[str, Any],
    extracted_text: str
) -> List[float]:
    client = OpenAI(
        api_key=os.getenv('OPENAI_API_KEY')
    )
    
    combined_input = f"Metadata: {metadata}\\nText: {extracted_text}"
    
    response = client.embeddings.create(
        input=combined_input,
        model='text-embedding-3-small'
    )
    
    return response.data[0].embedding
