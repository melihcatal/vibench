import google.generativeai as genai
import os
from typing import List, Dict, Any

def summarize_embedding_job_results(results: List[Dict[str, Any]]) -> str:
    """Summarizes the results of an embedding job using Google Gemini API.

    Args:
        results: A list of dictionaries, where each dictionary represents a result
                 (e.g., text and its embedding, or similarity scores).

    Returns:
        A string containing the summary of the embedding job results.
    """
    google_api_key = os.getenv("GOOGLE_API_KEY")
    if not google_api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")
    genai.configure(api_key=google_api_key)

    model = genai.GenerativeModel('gemini-pro') # Concrete model identifier

    # Convert results to a more readable string format for the LLM
    results_str = """Embedding job results:\n\n"""
    for i, res in enumerate(results):
        results_str += f"Result {i+1}:\n"
        for key, value in res.items():
            # Truncate long embedding vectors for summary to avoid exceeding context window
            if isinstance(value, list) and all(isinstance(x, (int, float)) for x in value):
                results_str += f"  {key}: [vector of length {len(value)}]\n"
            else:
                results_str += f"  {key}: {value}\n"
        results_str += "\n"

    prompt = f"""Please provide a concise summary of the following embedding job results. Highlight any key observations or patterns.

{results_str}

Summary:"""

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error summarizing results: {e}"

