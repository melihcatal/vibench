import os
import google.generativeai as genai
from typing import List, Dict


def embed_text_with_gemini(text: List[str]) -> Dict[str, List[List[float]]]:
    """
    Embeds text using the Gemini embeddings model.
    """
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")

    genai.configure(api_key=api_key)

    model_name = "models/embedding-001"

    # The embedding model can take a list of texts
    response = genai.embed_content(
        model=model_name,
        content=text,
        task_type="RETRIEVAL_DOCUMENT",  # or "RETRIEVAL_QUERY", "SEMANTIC_SIMILARITY", etc.
    )

    if response and response["embedding"]:
        return {"embeddings": response["embedding"]}
    else:
        raise Exception("Failed to generate embeddings or response was empty.")


if __name__ == "__main__":
    # Ensure GOOGLE_API_KEY is set in your environment
    if not os.environ.get("GOOGLE_API_KEY"):
        print("Please set the GOOGLE_API_KEY environment variable.")
    else:
        test_texts = [
            "The quick brown fox jumps over the lazy dog.",
            "A fast, brown fox leaps over a lethargic canine.",
            "This is a completely unrelated sentence.",
        ]

        print(f"Embedding texts: {test_texts}")
        try:
            embeddings_result = embed_text_with_gemini(test_texts)
            print("Embeddings generated successfully.")
            for i, embedding in enumerate(embeddings_result["embeddings"]):
                print(f"Embedding for text {i}: (first 5 elements) {embedding[:5]}...")
                print(f"Length of embedding {i}: {len(embedding)}")
        except Exception as e:
            print(f"Error generating embeddings: {e}")
