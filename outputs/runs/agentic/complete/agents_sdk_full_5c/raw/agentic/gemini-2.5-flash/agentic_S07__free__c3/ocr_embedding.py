import google.generativeai as genai
import os
from typing import List

def embed_text_sections(texts: List[str]) -> List[List[float]]:
    """Embeds extracted document sections for semantic retrieval using Google Generative AI (embedding-001).

    Args:
        texts: A list of text strings (document sections) to embed.

    Returns:
        A list of lists of floats, where each inner list is an embedding vector for a corresponding text.
    """
    # Ensure GOOGLE_API_KEY is set as an environment variable or configured
    # genai.configure(api_key="YOUR_API_KEY") # Uncomment and set your API key if not using env var

    # Using the 'embedding-001' model for text embeddings
    # Refer to https://ai.google.dev/docs/models_overview for available models.
    model = genai.GenerativeModel('embedding-001')

    embeddings = []
    for text in texts:
        result = model.embed_content(content=text, task_type="RETRIEVAL_DOCUMENT")
        embeddings.append(result['embedding'])
        
    return embeddings

if __name__ == '__main__':
    # Example usage (requires GOOGLE_API_KEY environment variable to be set)
    # os.environ["GOOGLE_API_KEY"] = "YOUR_API_KEY"
    # document_sections = [
    #     "The quick brown fox jumps over the lazy dog.",
    #     "A fast, reddish-brown canine leaps above a sluggish hound.",
    #     "The cat sat on the mat."
    # ]
    # 
    # vectors = embed_text_sections(document_sections)
    # print(f"Number of embeddings generated: {len(vectors)}")
    # if vectors:
    #     print(f"Dimension of first embedding: {len(vectors[0])}")
    #     print(f"First embedding (first 5 values): {vectors[0][:5]}...")
    pass
