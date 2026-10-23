import google.generativeai as genai
import os

def embed_platform_outputs(text: str, model_name: str = "models/embedding-001") -> dict:
    """
    Embeds platform outputs for evaluation or retrieval using Gemini Embeddings.
    
    Args:
        text: The text output from the model to embed.
        model_name: The name of the embedding model to use (e.g., "models/embedding-001").
        
    Returns:
        A dictionary containing the embedding vector and token count.
    """
    # Ensure GOOGLE_API_KEY is set in environment variables
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")
    
    genai.configure(api_key=api_key)

    response = genai.embed_content(
        model=model_name,
        content=text,
        task_type="RETRIEVAL_DOCUMENT" # or "SEMANTIC_SIMILARITY", "CLASSIFICATION", "CLUSTERING"
    )
    
    embedding_result = {
        "embedding": response['embedding'],
        "token_count": response['tokenCount'] if 'tokenCount' in response else None
    }
    return embedding_result

if __name__ == '__main__':
    # Example usage
    # os.environ["GOOGLE_API_KEY"] = "YOUR_GOOGLE_API_KEY" # Set your API key

    # print("Embedding a sample text...")
    # try:
    #     sample_text = "The quick brown fox jumps over the lazy dog."
    #     embedding_info = embed_platform_outputs(sample_text)
    #     print("Text:", sample_text)
    #     print("Embedding dimension:", len(embedding_info["embedding"]))
    #     print("First 5 embedding values:", embedding_info["embedding"][:5])
    #     print("Token count:", embedding_info["token_count"])
    #     
    #     print("\nEmbedding another text...")
    #     another_text = "A fast reddish-brown canid leaps over a sluggish canine."
    #     embedding_info_2 = embed_platform_outputs(another_text)
    #     print("Text:", another_text)
    #     print("Embedding dimension:", len(embedding_info_2["embedding"]))
    # except ValueError as e:
    #     print(f"Configuration error: {e}")
    # except Exception as e:
    #     print(f"Error during embedding: {e}")
