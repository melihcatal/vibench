import os
import google.generativeai as genai

def summarize_translation_quality_issues(original_text: str, translated_text: str, detected_issues: str) -> str:
    """Summarizes translation quality issues using Google Gemini API.

    Args:
        original_text: The original text.
        translated_text: The translated text.
        detected_issues: A string describing detected quality issues (e.g., from a QA tool).

    Returns:
        A summary of the translation quality issues.
    """
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    model = genai.GenerativeModel('gemini-pro')

    prompt = f"""Review the following original text and its translation, along with any detected quality issues. Provide a concise summary of the main quality problems and suggest potential improvements.

Original Text:
'''{original_text}'''

Translated Text:
'''{translated_text}'''

Detected Quality Issues:
'''{detected_issues}'''

Summary of Translation Quality Issues and Improvements:"""

    response = model.generate_content(prompt)
    return response.text

if __name__ == '__main__':
    # Example usage (requires GOOGLE_API_KEY env var)
    # original = "The quick brown fox jumps over the lazy dog."
    # translated = "El zorro rápido marrón salta sobre el perro perezoso."
    # issues = "Grammatical error: 'rápido marrón' should be 'marrón rápido'. Stylistic issue: 'salta sobre' is a bit literal, consider 'brinca sobre'."
    # summary = summarize_translation_quality_issues(original, translated, issues)
    # print(summary)
    pass
