import google.generativeai as genai
import os

def embed_text_sections(texts: list[str]):
    """Embeds a list of text sections using Gemini embeddings."""
    # Ensure GOOGLE_API_KEY is set in environment variables
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable must be set.")
    
    genai.configure(api_key=api_key)

    model = "models/embedding-001"
    
    # The SDK automatically handles batching if needed, but for simplicity
    # we'll assume a list of texts that can be processed.
    # For a production scenario, you might want to manually batch for large inputs.
    response = genai.embed_content(model=model, content=texts)
    
    embeddings = [embedding.values for embedding in response['embedding']]
    return embeddings

if __name__ == '__main__':
    # Set this environment variable for a real run
    # os.environ["GOOGLE_API_KEY"] = "YOUR_GEMINI_API_KEY"

    # texts_to_embed = [
    #     "The quick brown fox jumps over the lazy dog.",
    #     "Artificial intelligence is transforming industries.",
    #     "Machine learning models are trained on vast datasets."
    # ]
    # try:
    #     embeddings_list = embed_text_sections(texts_to_embed)
    #     for i, embedding in enumerate(embeddings_list):
    #         print(f"Embedding for text {i+1} (first 5 elements): {embedding[:5]}...")
    # except ValueError as e:
    #     print(f"Error: {e}. Please set GOOGLE_API_KEY environment variable.")
    pass
