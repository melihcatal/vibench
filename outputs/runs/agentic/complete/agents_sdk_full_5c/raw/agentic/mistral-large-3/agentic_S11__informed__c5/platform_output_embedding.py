from typing import List, Dict, Any
import cohere

def embed_platform_output(text: str) -> Dict[str, Any]:
    api_key = os.getenv("COHERE_API_KEY")
    co = cohere.Client(api_key)
    
    response = co.embed(
        texts=[text],
        model="embed-english-v3.0",
        input_type="search_document",
    )
    
    return {
        "embedding": response.embeddings[0],
        "model": "embed-english-v3.0",
        "input_text": text,
    }