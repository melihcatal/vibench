import os
import google.generativeai as genai
from typing import Dict, List, Union


def generate_metadata_embeddings(
    metadata: Dict[str, Union[str, int]], extracted_text: str
) -> List[float]:
    """
    Generates embeddings for a combination of object metadata and extracted text
    using the Google Gemini API.

    Requires the GOOGLE_API_KEY environment variable to be set.
    """
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")

    genai.configure(api_key=api_key)

    model = "models/embedding-001"

    # Combine metadata and text into a single string for embedding
    metadata_str = ", ".join([f"{key}: {value}" for key, value in metadata.items()])
    combined_text = f"Metadata: {metadata_str}\n\nContent: {extracted_text}"

    result = genai.embed_content(
        model=model, content=combined_text, task_type="retrieve_document"
    )

    return result["embedding"]
