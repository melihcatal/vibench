import os
import google.generativeai as genai


def summarize_quality(
    source_text: str, translated_text: str, target_language: str
) -> str:
    """
    Uses the Gemini API to provide a quality summary of a translation.

    Requires GOOGLE_API_KEY environment variable.
    """
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise EnvironmentError("GOOGLE_API_KEY environment variable not set.")

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-pro")

    prompt = f"""
    Analyze the quality of the following translation from English to {target_language}.
    Provide a brief, one-paragraph summary of any potential issues, such as awkward phrasing,
    mistranslations, or loss of nuance. If the translation is good, state that.

    Source Text:
    "{source_text}"

    Translated Text:
    "{translated_text}"

    Quality Summary:
    """

    response = model.generate_content(prompt)
    return response.text
