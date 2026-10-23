import os
import google.generativeai as genai
from typing import List, Dict, Any

def summarize_embedding_job_results(job_details: Dict[str, Any], embeddings_count: int, example_embedding: List[float]) -> str:
    """
    Summarizes the results of an embedding job using the Gemini generative model.
    This function takes embedding job details and uses a large language model
    to create a concise summary.
    """
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set for summarization.")
    genai.configure(api_key=api_key)
    
    # Using a suitable generative model for summarization
    model = genai.GenerativeModel('gemini-pro') # A powerful model for text generation

    prompt = f"""
    Summarize the following embedding job results.
    Job Details: {job_details}
    Total Embeddings Generated: {embeddings_count}
    Example Embedding (first 5 dimensions): {example_embedding[:5]}...
    Embedding Dimension: {len(example_embedding) if example_embedding else 'N/A'}

    Provide a concise summary highlighting the key aspects of this embedding job.
    """

    response = model.generate_content(prompt)
    return response.text

if __name__ == "__main__":
    # Ensure GOOGLE_API_KEY is set in your environment
    sample_job_details = {
        "job_id": "emb_job_001",
        "source": "customer_reviews.csv",
        "timestamp": "2023-10-27T10:00:00Z",
        "embedding_model": "models/text-embedding-004"
    }
    sample_embeddings_count = 1500
    sample_example_embedding = [0.01, 0.05, -0.03, 0.12, 0.08, 0.15, -0.07, 0.02, 0.11, -0.09] # 10 dimensions for example

    try:
        summary = summarize_embedding_job_results(
            sample_job_details,
            sample_embeddings_count,
            sample_example_embedding
        )
        print("Embedding Job Summary:")
        print(summary)
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An error occurred during summarization: {e}")
