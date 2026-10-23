import os
import google.generativeai as genai


def summarize_quality(
    source_text: str, translated_text: str, target_language: str
) -> str:
    """
    Uses the Gemini API to summarize translation quality issues.
    """
    genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
    model = genai.GenerativeModel("gemini-pro")

    prompt = f"""
    Analyze the quality of the following machine translation.
    Original Text (Source): "{source_text}"
    Translated Text (Target: {target_language}): "{translated_text}"

    Please provide a brief summary of potential quality issues. Consider fluency,
    accuracy, grammar, and any awkward phrasing. If the translation is good,
    state that.
    """

    response = model.generate_content(prompt)
    return response.text
