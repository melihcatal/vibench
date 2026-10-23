import os
import google.generativeai as genai
from typing import List, Dict, Any


def summarize_embedding_job_results(results: List[Dict[str, Any]]) -> str:
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")
    genai.configure(api_key=api_key)

    model = genai.GenerativeModel(
        "gemini-pro"
    )  # Using a generative model for summarization

    # Convert results to a string format for the LLM
    results_str = """
    Here are the results of an embedding job:

    """
    for i, result in enumerate(results):
        results_str += f"Item {i + 1}:\n"
        for key, value in result.items():
            results_str += f"  {key}: {value}\n"
        results_str += "\n"

    prompt = f"Please summarize the following embedding job results:\n\n{results_str}\nSummary:"

    response = model.generate_content(prompt)
    return response.text
