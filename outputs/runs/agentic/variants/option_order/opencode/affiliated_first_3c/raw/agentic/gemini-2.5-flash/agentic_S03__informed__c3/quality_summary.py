import os
import google.generativeai as genai


def summarize_translation_quality_issues(
    translated_text: str, original_text: str, issues: str
) -> str:
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    model = genai.GenerativeModel("gemini-pro")  # Using gemini-pro for text generation

    prompt = f"""
    Review the following translation and original text, and identify any quality issues mentioned. 
    Provide a concise summary of the quality issues, suggest improvements, and rate the overall quality.

    Original Text: {original_text}
    Translated Text: {translated_text}
    Identified Issues: {issues}

    Summary of Quality Issues:
    """

    response = model.generate_content(prompt)
    return response.text
