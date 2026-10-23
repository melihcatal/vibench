import os
import google.generativeai as genai
from typing import List, Dict


def summarize_embedding_job_results(job_results: List[Dict]) -> str:
    """
    Summarizes embedding job results using the Google Gemini API (hosted LLM).
    """
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set for Gemini API.")

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(
        "gemini-pro"
    )  # Google Gemini Pro model for text generation

    prompt = f"""Summarize the following embedding job results. Highlight key statistics,
                 any anomalies, or notable patterns.
                 
                 Embedding Job Results:
                 {job_results}
                 
                 Summary:"""

    response = model.generate_content(prompt)
    return response.text


if __name__ == "__main__":
    # Example job results (in a real scenario, this would come from an actual embedding job)
    sample_job_results = [
        {
            "text_id": "doc1",
            "embedding_length": 768,
            "status": "completed",
            "processing_time_ms": 120,
        },
        {
            "text_id": "doc2",
            "embedding_length": 768,
            "status": "completed",
            "processing_time_ms": 150,
        },
        {
            "text_id": "doc3",
            "embedding_length": 768,
            "status": "failed",
            "error": "text too long",
            "processing_time_ms": 50,
        },
        {
            "text_id": "doc4",
            "embedding_length": 768,
            "status": "completed",
            "processing_time_ms": 130,
        },
    ]

    summary = summarize_embedding_job_results(sample_job_results)
    print("Embedding Job Summary:")
    print(summary)
