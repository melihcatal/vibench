import os
import openai

def get_text_embedding(text: str, model: str = "text-embedding-ada-002") -> list[float]:
    """Embeds transcript segments for semantic retrieval using OpenAI Embeddings."""
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")

    # Ensure the API key is set for the openai client
    openai.api_key = api_key

    response = openai.embeddings.create(
        input=[text],
        model=model
    )
    return response.data[0].embedding

if __name__ == '__main__':
    # Set OPENAI_API_KEY environment variable
    # For example: export OPENAI_API_KEY="YOUR_OPENAI_API_KEY"
    example_segment_1 = "The cat sat on the mat."
    example_segment_2 = "The dog lay on the rug."
    example_segment_3 = "Artificial intelligence is transforming industries."

    try:
        embedding_1 = get_text_embedding(example_segment_1)
        embedding_2 = get_text_embedding(example_segment_2)
        embedding_3 = get_text_embedding(example_segment_3)

        print(f"Embedding for \"{example_segment_1}\" (first 5 dimensions): {embedding_1[:5]}...")
        print(f"Embedding for \"{example_segment_2}\" (first 5 dimensions): {embedding_2[:5]}...")
        print(f"Embedding for \"{example_segment_3}\" (first 5 dimensions): {embedding_3[:5]}...")

        # You could then calculate similarity between these embeddings
        # For example, using cosine similarity.

    except Exception as e:
        print(f"Error getting embeddings: {e}")
