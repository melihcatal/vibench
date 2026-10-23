import os
import google.generativeai as genai

def get_text_embedding(text: str) -> list[float]:
    google_api_key = os.environ.get("GOOGLE_API_KEY")

    if not google_api_key:
        raise ValueError("Please set GOOGLE_API_KEY environment variable.")

    genai.configure(api_key=google_api_key)

    # Using the embedding-001 model for embeddings
    try:
        response = genai.embed_content(model="models/embedding-001", content=text)
        return response['embedding']
    except Exception as e:
        print(f"Error getting embedding: {e}")
        return []

if __name__ == "__main__":
    # Example usage
    caption_chunk_1 = "The meeting focused on budget allocation and project timelines."
    embedding_1 = get_text_embedding(caption_chunk_1)
    print(f"\nEmbedding for \"{caption_chunk_1}\": {embedding_1[:10]}... (truncated to first 10 dimensions)")
    print(f"Embedding length: {len(embedding_1)}")

    caption_chunk_2 = "Sarah presented the marketing strategy and Q3 financial forecasts."
    embedding_2 = get_text_embedding(caption_chunk_2)
    print(f"\nEmbedding for \"{caption_chunk_2}\": {embedding_2[:10]}... (truncated to first 10 dimensions)")
    print(f"Embedding length: {len(embedding_2)}")

    caption_chunk_3 = "Financial planning for the third quarter and marketing initiatives were discussed."
    embedding_3 = get_text_embedding(caption_chunk_3)
    print(f"\nEmbedding for \"{caption_chunk_3}\": {embedding_3[:10]}... (truncated to first 10 dimensions)")
    print(f"Embedding length: {len(embedding_3)}")

    # You could then use these embeddings for similarity search, clustering, etc.
