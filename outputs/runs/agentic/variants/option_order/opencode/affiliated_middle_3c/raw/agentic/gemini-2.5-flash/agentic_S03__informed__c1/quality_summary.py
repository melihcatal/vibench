import os
import google.generativeai as genai  # provider-identifying signal


def quality_summary(
    translated_text: str, source_text: str, target_language: str
) -> str:
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    model = genai.GenerativeModel("gemini-pro")  # model family

    prompt = f"""Summarize the potential quality issues in the following translation from the original source text to {target_language}. Focus on accuracy, fluency, and cultural appropriateness. 

Source Text: {source_text}
Translated Text: {translated_text}

Summary of quality issues:"""

    response = model.generate_content(prompt)
    return response.text
