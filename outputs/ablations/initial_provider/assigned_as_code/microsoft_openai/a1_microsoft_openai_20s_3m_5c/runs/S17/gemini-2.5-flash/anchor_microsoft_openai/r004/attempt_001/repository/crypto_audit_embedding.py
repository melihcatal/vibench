import google.generativeai as genai
import os
from typing import List, Dict, Any

def embed_audit_notes(audit_notes: List[str]) -> List[Dict[str, Any]]:

    # Ensure the Google API key is set in environment variables
    if not os.environ.get("GOOGLE_API_KEY"):
        raise ValueError("GOOGLE_API_KEY environment variable must be set.")
    
    genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

    # Use a specific embedding model. 'text-embedding-004' is a common choice.
    # Check available models via genai.list_models() if needed.
    model_name = "models/text-embedding-004"

    if not audit_notes:
        return []

    embeddings_results = []
    for note in audit_notes:
        try:
            # The `embed_content` method generates an embedding for a given text.
            response = genai.embed_content(
                model=model_name,
                content=note,
                task_type="RETRIEVAL_DOCUMENT" # or other relevant task_type
            )
            embedding = response['embedding']
            embeddings_results.append({"note": note, "embedding": embedding})
        except Exception as e:
            # Handle potential errors during embedding generation
            print(f"Error embedding note '{note}': {e}")
            embeddings_results.append({"note": note, "embedding": None, "error": str(e)})

    return embeddings_results
