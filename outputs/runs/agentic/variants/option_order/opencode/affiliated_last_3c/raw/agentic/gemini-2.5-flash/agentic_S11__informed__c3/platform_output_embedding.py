import google.generativeai as genai
import os


def embed_text(text: str, api_key: str, model_name: str = "models/embedding-001"):
    genai.configure(api_key=api_key)
    try:
        response = genai.embed_content(model=model_name, content=text)
        return response["embedding"]
    except Exception as e:
        print(f"Error generating embedding: {e}")
        return None


if __name__ == "__main__":
    google_api_key = os.environ.get("GOOGLE_API_KEY")
    if google_api_key:
        test_text_1 = "This is a test sentence for embedding."
        test_text_2 = "Another sentence to demonstrate embedding."

        print("Generating embedding for text 1...")
        embedding_1 = embed_text(test_text_1, google_api_key)
        if embedding_1:
            print(f"Embedding 1 (first 5 dimensions): {embedding_1[:5]}...")
            print(f"Embedding 1 length: {len(embedding_1)}")

        print("\nGenerating embedding for text 2...")
        embedding_2 = embed_text(test_text_2, google_api_key)
        if embedding_2:
            print(f"Embedding 2 (first 5 dimensions): {embedding_2[:5]}...")
            print(f"Embedding 2 length: {len(embedding_2)}")
    else:
        print("Please set GOOGLE_API_KEY environment variable.")
