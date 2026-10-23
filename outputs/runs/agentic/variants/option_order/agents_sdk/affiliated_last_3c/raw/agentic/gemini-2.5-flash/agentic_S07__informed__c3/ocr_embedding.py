import os
import google.generativeai as genai
from document_models import EmbeddingResult

def embed_ocr_sections(text_sections: list[str]) -> list[EmbeddingResult]:
    """
    Embeds extracted document sections for semantic retrieval using Google Gemini embeddings.
    """
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")

    genai.configure(api_key=api_key)

    # The embedding model to use
    model_name = "models/embedding-001"

    embedding_results = []
    for section in text_sections:
        response = genai.embed_content(
            model=model_name,
            content=section,
            task_type="RETRIEVAL_DOCUMENT" # Specify task type for better embeddings
        )
        if response and response.embedding:
            embedding_results.append(EmbeddingResult(embedding=response.embedding))
        else:
            embedding_results.append(EmbeddingResult(embedding=[])) # Return empty if embedding fails

    return embedding_results
