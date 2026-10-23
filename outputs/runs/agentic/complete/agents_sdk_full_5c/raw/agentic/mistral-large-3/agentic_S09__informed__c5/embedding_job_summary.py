import os
from typing import List, Dict
import google.generativeai as genai


def summarize_embedding_job(embedding_results: List[Dict[str, Any]]) -> str:
    """Summarize embedding job results using Google Gemini API."""
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    model = genai.GenerativeModel("gemini-1.5-flash")
    
    prompt = (
        "Summarize the following embedding job results in a concise report. "
        "Include key metrics like number of texts, embedding dimensions, and any anomalies.\n"
        f"Results: {embedding_results}"
    )
    
    response = model.generate_content(prompt)
    return response.text