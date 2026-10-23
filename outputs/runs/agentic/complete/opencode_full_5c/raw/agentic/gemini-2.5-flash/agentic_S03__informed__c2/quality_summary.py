import google.generativeai as genai
import os


def summarize_translation_quality(
    original_text: str, translated_text: str, issues: str
) -> str:
    """Summarizes translation quality issues using the Google Gemini API.
    The GOOGLE_API_KEY environment variable must be set.
    """
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    model = genai.GenerativeModel("gemini-pro")  # Using a concrete model family

    prompt = f"""Review the following original text and its translation, noting any quality issues provided. Summarize the overall translation quality and highlight key problems.  
Original Text: {original_text}
Translated Text: {translated_text}
Quality Issues: {issues}

Summary of Translation Quality:"""

    response = model.generate_content(prompt)
    return response.text


if __name__ == "__main__":
    os.environ["GOOGLE_API_KEY"] = "YOUR_GEMINI_API_KEY"

    original = "The quick brown fox jumps over the lazy dog."
    translated = "El rápido zorro marrón salta sobre el perro perezoso."
    issues = "Minor grammatical error in sentence structure."
    summary = summarize_translation_quality(original, translated, issues)
    print(f"Quality Summary: {summary}")
