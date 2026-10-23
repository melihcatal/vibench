import os
import google.generativeai as genai
from typing import List


def summarize_incident(error_logs: List[str]) -> str:
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-pro")

    log_text = "\n".join(error_logs)
    prompt = f"Summarize the following error logs for an incident review, identifying key issues, potential root causes, and affected components:\n\n{log_text}\n\nSummary:"

    response = model.generate_content(prompt)
    return response.text
