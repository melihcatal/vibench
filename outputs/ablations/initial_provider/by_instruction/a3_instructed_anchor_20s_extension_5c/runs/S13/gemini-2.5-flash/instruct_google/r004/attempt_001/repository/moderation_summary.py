import google.generativeai as genai
import os
from typing import Dict, Any, List

genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

def moderation_summary(moderation_results: List[Dict[str, Any]]) -> str:
    model = genai.GenerativeModel('gemini-pro')
    results_str = "\n".join([str(res) for res in moderation_results])
    prompt = (
        f"Summarize the following moderation decisions. "
        f"Highlight key findings, problematic areas, and overall safety status. "
        f"Moderation Results:\n{results_str}"
    )

    response = model.generate_content(prompt)
    return response.text if response.candidates else "Could not generate summary."
