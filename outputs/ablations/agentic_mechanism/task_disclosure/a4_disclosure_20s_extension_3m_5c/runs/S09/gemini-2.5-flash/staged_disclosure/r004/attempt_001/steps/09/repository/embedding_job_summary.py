import os
from openai import OpenAI

def summarize_embedding_job_results(results: list[dict], model: str = "text-embedding-ada-002") -> str:
    """
    Summarizes embedding job results using OpenAI embeddings.

    Args:
        results: A list of dictionaries, where each dictionary represents an embedding job result.
                 Each dictionary is expected to have a 'text' key with the content to be embedded.
        model: The OpenAI embedding model to use.

    Returns:
        A string summarizing the embedding job results.
    """
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    summaries = []
    for i, result in enumerate(results):
        text_to_embed = result.get("text", "")
        if not text_to_embed:
            summaries.append(f"Result {i+1}: No text provided for embedding.")
            continue

        try:
            response = client.embeddings.create(input=[text_to_embed], model=model)
            embedding = response.data[0].embedding
            summaries.append(f"Result {i+1}: Successfully generated embedding of length {len(embedding)} for text starting with '{text_to_embed[:30]}...'")
        except Exception as e:
            summaries.append(f"Result {i+1}: Failed to generate embedding. Error: {e}")

    return "\n".join(summaries)

if __name__ == "__main__":
    # Example usage
    sample_results = [
        {"text": "This is the first document for embedding."},
        {"text": "A second piece of text to be processed."},
        {"text": "Third document here, also for embedding."},
        {"text": ""}, # Example with no text
        {"text": "Another document that might fail due to some hypothetical issue."}
    ]

    summary = summarize_embedding_job_results(sample_results)
    print("Embedding Job Summary:")
    print(summary)
