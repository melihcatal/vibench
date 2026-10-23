import os
from typing import List
import google.generativeai as genai


def summarize_transcription_results(full_transcript: str) -> str:
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    model = genai.GenerativeModel("gemini-pro")

    prompt = f"Please provide a concise summary of the following transcript:\n\n{full_transcript}"

    response = model.generate_content(prompt)

    return response.text
