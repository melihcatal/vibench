import os
import google.generativeai as genai


def quality_summary(
    source_text: str, translated_text: str, source_lang: str, target_lang: str
) -> str:
    """
    Summarizes potential quality issues in a translation using Gemini.
    """
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")

    genai.configure(api_key=api_key)

    model = genai.GenerativeModel("gemini-pro")

    prompt = f"""
    Analyze the following translation for quality issues.
    Source Text ({source_lang}): "{source_text}"
    Translated Text ({target_lang}): "{translated_text}"

    Please provide a brief summary of potential issues, such as:
    - Mistranslations
    - Grammatical errors
    - Awkward phrasing
    - Loss of nuance or tone

    If there are no obvious issues, state that the translation appears to be of good quality.
    Summary:
    """

    response = model.generate_content(prompt)
    return response.text
