import google.generativeai as genai
import os

def embed_script(script_text: str, model_name: str = "models/text-embedding-004"):
    """
    Embeds narration scripts for voice-asset search using Gemini Embeddings.
    Requires GOOGLE_API_KEY environment variable.
    """
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("Please set the GOOGLE_API_KEY environment variable.")

    genai.configure(api_key=api_key)

    try:
        # For a single text input, use embed_content directly
        response = genai.embed_content(
            model=model_name,
            content=script_text,
            task_type="SEMANTIC_SIMILARITY"
        )
        embedding = response["embedding"]
        print(f"Script embedded successfully. Embedding length: {len(embedding)}")
        # print(f"Embedding (first 5 elements): {embedding[:5]}...") # Uncomment for debugging
        return embedding
    except Exception as e:
        print(f"Error embedding script with Gemini: {e}")
        return None

if __name__ == "__main__":
    # Example usage (ensure GOOGLE_API_KEY is set)
    # os.environ["GOOGLE_API_KEY"] = "YOUR_GEMINI_API_KEY"

    # script = "This is a script about a brave knight and a fierce dragon."
    # print(f"Embedding script: '{script}'")
    # embedding = embed_script(script)
    # if embedding:
    #     print("Embedding generated.")

    print("To run this example, please set the GOOGLE_API_KEY environment variable.")
    print("Embedding a dummy script:")
    dummy_embedding = embed_script("The quick brown fox jumps over the lazy dog.")
    if dummy_embedding:
        print("Dummy embedding generated.")
