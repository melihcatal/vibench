import os
import google.generativeai as genai
from typing import Dict, Any


def summarize_embedding_job(job_results: Dict[str, Any]) -> str:
    """
    Summarizes the results of an embedding job using Google Gemini.
    """
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")

    genai.configure(api_key=api_key)

    model = genai.GenerativeModel("gemini-pro")

    num_embeddings = len(job_results.get("embeddings", []))
    if num_embeddings == 0:
        return "The embedding job produced no results."

    first_embedding = job_results["embeddings"][0]
    dimensionality = len(first_embedding)

    prompt = f"""
    An embedding job has completed. Here are the statistics:
    - Number of vectors generated: {num_embeddings}
    - Vector dimensionality: {dimensionality}

    Please provide a brief, one-sentence summary of this embedding job's output.
    Focus on the scale and nature of the data produced.
    """

    response = model.generate_content(prompt)
    return response.text.strip()


if __name__ == "__main__":
    # This is an example and will not be executed
    mock_job_results = {
        "embeddings": [[0.1] * 1024, [0.2] * 1024, [0.3] * 1024],
        "model": "embed-english-v3.0",
    }
    summary = summarize_embedding_job(mock_job_results)
    print(summary)
