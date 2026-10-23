import os
import google.generativeai as genai  # Provider-identifying signal


def summarize_embedding_job_results(job_results: str) -> str:
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-pro")  # Concrete model identifier

    prompt = f"""Summarize the following embedding job results:

{job_results}

Provide a concise summary highlighting key outcomes and any notable observations.
"""

    response = model.generate_content(prompt)
    return response.text
