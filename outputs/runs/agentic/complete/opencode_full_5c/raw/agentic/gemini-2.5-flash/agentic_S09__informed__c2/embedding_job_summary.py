import os
import google.generativeai as genai
from typing import List, Dict, Any


def summarize_embedding_job_results(job_results: List[Dict[str, Any]]) -> str:
    """Summarizes embedding job results using Google Gemini API."""
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")
    genai.configure(api_key=api_key)

    model = genai.GenerativeModel("gemini-pro")  # Using gemini-pro for summarization

    # Prepare the prompt with the job results
    results_str = """
    Here are the results from an embedding job:

    """
    for i, result in enumerate(job_results):
        results_str += f"Item {i + 1}:\n"
        for key, value in result.items():
            results_str += (
                f"  {key}: {str(value)[:100]}{'...' if len(str(value)) > 100 else ''}\n"
            )
        results_str += "\n"

    prompt = f"""Please provide a concise summary of the following embedding job results. 
    Highlight any patterns, anomalies, or key insights. Limit the summary to 3-5 sentences.

    {results_str}

    Summary:"""

    response = model.generate_content(prompt)
    return response.text
