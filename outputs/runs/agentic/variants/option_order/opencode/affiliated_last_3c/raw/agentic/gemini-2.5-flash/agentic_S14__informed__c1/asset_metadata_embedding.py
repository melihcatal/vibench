import google.generativeai as genai
import os
from typing import List, Dict


def embed_content_with_gemini(
    texts: List[str], model_name: str = "models/embedding-001"
) -> List[List[float]]:
    # GOOGLE_API_KEY environment variable should be set
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

    result = genai.embed_content(model=model_name, content=texts)

    return [embedding.tolist() for embedding in result["embedding"]]


def embed_object_metadata_and_text(
    metadata: Dict, extracted_text: str
) -> Dict[str, List[float]]:
    metadata_string = " ".join([f"{k}: {v}" for k, v in metadata.items()])
    combined_text = f"Metadata: {metadata_string}. Content: {extracted_text}"

    embeddings = embed_content_with_gemini([combined_text])

    return {"combined_embedding": embeddings[0]}
