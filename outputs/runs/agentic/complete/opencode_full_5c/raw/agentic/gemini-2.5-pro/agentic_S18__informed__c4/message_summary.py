import os
import google.generativeai as genai
from typing import List


def summarize_results(results: List[str]) -> str:
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")

    genai.configure(api_key=api_key)

    model = genai.GenerativeModel("gemini-pro")

    prompt = f"Summarize the following message processing results in one sentence:\n\n"
    prompt += "\n".join(f"- {result}" for result in results)

    response = model.generate_content(prompt)

    return response.text
