import os
import google.generativeai as genai
from typing import List

def embed_script(script_texts: List[str]) -> List[List[float]]:
    """Embeds narration scripts for voice-asset search using Gemini Embeddings."""
    # Ensure GOOGLE_API_KEY environment variable is set
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable must be set for Gemini Embeddings.")
    
    genai.configure(api_key=api_key)

    # The embedding model to use. You can choose different models like 'embedding-001'
    # or other specific embedding models provided by Gemini.
    model_name = "models/embedding-001"

    embeddings = []
    for text in script_texts:
        # The task_type here is set to retrieval_document. Other options include retrieval_query, semantic_similarity, etc.
        # This choice affects how the embedding is generated and should match the intended use case.
        response = genai.embed_content(
            model=model_name,
            content=text,
            task_type="retrieval_document"
        )
        embeddings.append(response['embedding'])
    
    return embeddings

if __name__ == "__main__":
    # Example usage (ensure GOOGLE_API_KEY is set)
    # os.environ["GOOGLE_API_KEY"] = "YOUR_GEMINI_API_KEY"

    scripts = [
        "This is the first part of a narration about ancient history.",
        "The second part discusses modern technological advancements.",
        "A different script entirely, perhaps about cooking recipes."
    ]

    try:
        script_embeddings = embed_script(scripts)
        print(f"Generated {len(script_embeddings)} embeddings.")
        if script_embeddings:
            print(f"First embedding dimension: {len(script_embeddings[0])}")
            print(f"First embedding (first 5 values): {script_embeddings[0][:5]}...")
    except ValueError as e:
        print(f"Error embedding scripts: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}. Make sure the API key is valid and the model is accessible.")
