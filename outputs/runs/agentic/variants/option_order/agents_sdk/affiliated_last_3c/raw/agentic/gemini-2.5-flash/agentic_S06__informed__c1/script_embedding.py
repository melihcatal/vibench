import google.generativeai as glm
import os
from typing import List, Dict

def embed_narration_scripts(scripts: List[str], model_name: str = "embedding-001") -> List[Dict]:
    """
    Embeds narration scripts into vector representations using Gemini Embeddings.
    
    Args:
        scripts: A list of narration script strings to embed.
        model_name: The name of the embedding model to use (e.g., "embedding-001").
        
    Returns:
        A list of dictionaries, where each dictionary contains the original text
        and its corresponding embedding vector.
    """
    # Ensure GOOGLE_API_KEY is set in environment variables
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        print("Error: GOOGLE_API_KEY environment variable is not set. Cannot use Gemini Embeddings.")
        return []

    glm.configure(api_key=api_key)

    embeddings_results = []
    for script in scripts:
        try:
            # The embed_content function takes content and an optional task_type
            response = glm.embed_content(model=model_name, content=script)
            embeddings_results.append({
                "original_text": script,
                "embedding": response['embedding']
            })
        except Exception as e:
            print(f"Error embedding script \"{script[:50]}...\": {e}")
            embeddings_results.append({
                "original_text": script,
                "embedding": None # Indicate failure for this script
            })
            
    return embeddings_results

if __name__ == '__main__':
    # Set your Google API Key as an environment variable:
    # export GOOGLE_API_KEY="YOUR_GEMINI_API_KEY"
    
    sample_scripts = [
        "The quick brown fox jumps over the lazy dog.",
        "A group of canines rests peacefully under the afternoon sun.",
        "High-definition audio offers an immersive listening experience.",
        "Voice assets are crucial for rich media production."
    ]
    
    print("Embedding narration scripts...")
    embeddings = embed_narration_scripts(sample_scripts)
    
    if embeddings:
        for result in embeddings:
            if result['embedding']:
                print(f"Original Text: \"{result['original_text']}\"")
                print(f"Embedding (first 5 dims): {result['embedding'][:5]}...")
                print(f"Embedding Dimension: {len(result['embedding'])}")
            else:
                print(f"Original Text: \"{result['original_text']}\" - Embedding failed.")
            print("-" * 30)
    else:
        print("No embeddings generated.")
