import os
import google.generativeai as genai


def embed_caption_chunks(caption_chunks: list[str]) -> list[list[float]]:
    """
    Embeds caption chunks for semantic meeting search using Gemini embeddings.

    Args:
        caption_chunks (list[str]): A list of caption chunks (strings).

    Returns:
        list[list[float]]: A list of embedding vectors, one for each caption chunk.
    """
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError(
            "Google API key not provided and GOOGLE_API_KEY env var is not set."
        )
    genai.configure(api_key=api_key)

    # Using the embedding model for text embeddings
    model = "models/embedding-001"

    embeddings = []
    for chunk in caption_chunks:
        try:
            response = genai.embed_content(
                model=model, content=chunk, task_type="SEMANTIC_SIMILARITY"
            )
            embeddings.append(response["embedding"])
            print(
                f"Embedded chunk: '{chunk}' (first 5 dimensions: {response['embedding'][:5]}...)"
            )
        except Exception as e:
            print(f"Error embedding chunk '{chunk}': {e}")
            embeddings.append([])  # Append an empty list or handle error as appropriate

    return embeddings


if __name__ == "__main__":
    # This part is for local testing and won't be part of the scored submission.
    # Make sure to set GOOGLE_API_KEY environment variable
    # os.environ["GOOGLE_API_KEY"] = "your-gemini-api-key"
    # mock_captions = [
    #     "The quarterly financial results were presented.",
    #     "We need to focus on increasing sales in the European market.",
    #     "The marketing team will launch a new campaign next month.",
    #     "The product roadmap for next year was also discussed."
    # ]
    # try:
    #     caption_embeddings = embed_caption_chunks(mock_captions)
    #     print(f"Generated embeddings for captions: {len(caption_embeddings)} embeddings.")
    #     if caption_embeddings:
    #         print(f"First embedding (first 5 dimensions): {caption_embeddings[0][:5]}")
    # except ValueError as e:
    #     print(f"Error: {e}")
    pass
