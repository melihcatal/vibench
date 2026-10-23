import os
import google.generativeai as genai
from typing import List, Dict, Any

LLM_MODEL = "gemini-pro"


def summarize_embedding_job_results(job_results: List[Dict[str, Any]]) -> str:
    """Summarizes embedding job results using Google Gemini API."""
    genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
    model = genai.GenerativeModel(LLM_MODEL)

    # Convert job_results to a string format suitable for summarization
    job_results_str = "Embedding Job Results:\n"
    for i, result in enumerate(job_results):
        job_results_str += f"Job {i + 1}:\n"
        for key, value in result.items():
            job_results_str += (
                f"  {key}: {str(value)[:100]}...\n"  # Truncate long values
            )
        job_results_str += "\n"

    prompt = f"Please provide a concise summary of the following embedding job results:\n\n{job_results_str}"

    response = model.generate_content(prompt)
    return response.text
