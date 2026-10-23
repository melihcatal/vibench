import os
import google.generativeai as genai
from typing import List, Dict, Any


def summarize_embedding_job_results(job_results: List[Dict[str, Any]]) -> str:
    """
    Summarizes embedding job results using the Google Gemini API.
    """
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    model = genai.GenerativeModel("gemini-pro")

    # Simple concatenation for demonstration. In a real scenario, you might want to process
    # the job_results more intelligently to provide a concise summary.
    texts = [result.get("text", "") for result in job_results if "text" in result]
    summary_prompt = (
        f"Summarize the following texts from an embedding job: {'; '.join(texts)}"
    )

    response = model.generate_content(summary_prompt)
    return response.text
