import google.generativeai as genai
import os
from typing import List, Dict, Any

# Ensure GOOGLE_API_KEY is set in your environment
# genai.configure(api_key="YOUR_GOOGLE_API_KEY") # Better to use environment variable

def embed_moderation_rationales(rationales: List[str]) -> List[List[float]]:
    """
    Embed moderation rationales (reasons for decisions) for case retrieval using Google Generative AI.

    Args:
        rationales: A list of strings, where each string is a moderation rationale.

    Returns:
        A list of embedding vectors (list of floats), one for each rationale.
    """
    if not genai.configure(api_key=os.environ.get("GOOGLE_API_KEY")):
        raise ValueError("GOOGLE_API_KEY environment variable not set. Please set it to use Generative AI.")

    model_name = "embedding-001" # Or other suitable embedding model like text-embedding-004
    
    # The Google Generative AI SDK treats embedding models similarly to chat models for generation,
    # but the method call is specific to embeddings.
    # For embedding-001, we use genai.embed_content directly.
    
    embeddings = []
    for rationale in rationales:
        try:
            # The 'task_type' and 'title' are optional but can improve embedding quality
            # for specific use cases.
            response = genai.embed_content(
                model=model_name,
                content=rationale,
                task_type="RETRIEVAL_DOCUMENT" # Or RETRIEVAL_QUERY depending on use case
            )
            embeddings.append(response['embedding'])
        except Exception as e:
            print(f"Error embedding rationale '{rationale}': {e}")
            embeddings.append([]) # Append an empty list or None to indicate failure
    
    return embeddings

if __name__ == '__main__':
    # Set a dummy API key for local testing reminder
    os.environ["GOOGLE_API_KEY"] = os.environ.get("GOOGLE_API_KEY", "YOUR_GEMINI_API_KEY_HERE")

    example_rationales = [
        "Content contained severe hate speech and incitement to violence.",
        "The text was detected as spam with a high confidence score.",
        "User appeal for a false positive, reviewed and approved.",
        "Mild language violation, issued a warning.",
        "No policy violations found after manual review."
    ]

    embeddings = embed_moderation_rationales(example_rationales)
    
    print("\nEmbeddings for Moderation Rationales:")
    for i, emb in enumerate(embeddings):
        if emb:
            print(f"  Rationale {i+1} (Vector Length {len(emb)}): {emb[:5]}...") # Print first 5 elements
        else:
            print(f"  Rationale {i+1}: Embedding failed.")
