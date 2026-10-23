import google.generativeai as genai
import os
from typing import List, Dict

def summarize_embedding_job_results(job_details: Dict, embedding_results: List[List[float]], top_n_texts: List[str]) -> str:
    """Summarizes the results of an embedding job using Google Gemini API.

    Args:
        job_details: Dictionary containing details about the embedding job (e.g., input size, model used).
        embedding_results: A sample or representative subset of the generated embeddings.
        top_n_texts: Top N texts identified by similarity or other metrics after embedding.

    Returns:
        A string summary of the embedding job results.
    """
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    model = genai.GenerativeModel('gemini-pro') # Using a generative model for summarization

    prompt = f"""Summarize the following embedding job results. 
    Job Details: {job_details}
    Sample Embeddings (first few elements of first 2 embeddings): {embedding_results[:2]}
    Top identified texts: {top_n_texts}

    Provide a concise summary highlighting key aspects and potential insights.
    """

    response = model.generate_content(prompt)
    return response.text

if __name__ == '__main__':
    # Dummy data for demonstration
    job_details = {
        "input_count": 1000,
        "model": "models/embedding-001",
        "task_type": "RETRIEVAL_DOCUMENT",
        "processing_time_sec": 120
    }
    sample_embeddings = [
        [0.1, 0.2, 0.3, 0.4, 0.5],
        [0.6, 0.7, 0.8, 0.9, 1.0]
    ]
    top_texts = [
        "The quick brown fox.",
        "Lazy dog sleeps."
    ]

    try:
        summary = summarize_embedding_job_results(job_details, sample_embeddings, top_texts)
        print("Embedding Job Summary:")
        print(summary)
    except Exception as e:
        print(f"Error generating summary: {e}")
        print("Please ensure GOOGLE_API_KEY is set and you have access to gemini-pro.")
