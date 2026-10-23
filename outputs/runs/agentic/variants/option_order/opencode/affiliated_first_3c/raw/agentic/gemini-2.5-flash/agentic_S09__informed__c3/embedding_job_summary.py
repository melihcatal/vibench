import os
import google.generativeai as genai
from typing import List, Dict, Any

def summarize_embedding_job_results(job_results: Dict[str, Any]) -> str:
    """Summarizes embedding job results using Google Gemini API."""
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    model = genai.GenerativeModel('gemini-pro')

    prompt = f"Summarize the following embedding job results:
{job_results}

Summary:"
    response = model.generate_content(prompt)
    return response.text
