import google.generativeai as genai
import os

def summarize_translation_quality(source_text: str, translated_text: str, source_language: str, target_language: str) -> str:
    # Configure the Google Gemini API client
    # Ensure GOOGLE_API_KEY environment variable is set
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    model = genai.GenerativeModel('gemini-pro') # Using a concrete model ID

    prompt = f"""Analyze the following translation from {source_language} to {target_language} for quality issues. Provide a concise summary of any potential problems, inaccuracies, or areas for improvement.

Source Text: """{source_text}"""

Translated Text: """{translated_text}"""

Summary of quality issues:"""

    response = model.generate_content(prompt)
    return response.text
