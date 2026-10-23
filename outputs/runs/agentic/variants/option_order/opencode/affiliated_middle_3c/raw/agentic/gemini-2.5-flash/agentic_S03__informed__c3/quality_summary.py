import os
import google.generativeai as genai
from typing import Dict

def summarize_translation_quality(translated_content: Dict[str, str], source_lang: str, target_lang: str) -> str:
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")
    genai.configure(api_key=api_key)

    model = genai.GenerativeModel('gemini-pro')

    prompt = f"Summarize the potential quality issues in the following {source_lang} to {target_lang} translations:
"
    for key, value in translated_content.items():
        prompt += f"Key: {key}, Translated Value: {value}
"
    prompt += "Focus on accuracy, fluency, and cultural appropriateness."

    response = model.generate_content(prompt)
    return response.text
