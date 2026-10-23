import os
import google.generativeai as genai

def summarize_translation_quality(source_text: str, translated_text: str, target_language: str) -> str:
    """Summarizes translation quality issues using Google Gemini API."""
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    model = genai.GenerativeModel('gemini-pro')

    prompt = f"""Analyze the quality of the following translation from the original text to {target_language}. ""
             f"""Identify any potential issues such as inaccuracies, grammatical errors, unnatural phrasing, or missed nuances.""
             f"""Provide a concise summary of the translation quality and suggest improvements if any."""
             f"""Original Text: \"\"\"{source_text}\""\"
             f"""Translated Text: \"\"\"{translated_text}\""\"

    response = model.generate_content(prompt)
    return response.text

if __name__ == '__main__':
    # Set GOOGLE_API_KEY environment variable
    original = "The quick brown fox jumps over the lazy dog."
    translated = "Der schnelle braune Fuchs springt über den faulen Hund."
    summary = summarize_translation_quality(original, translated, "German")
    print(f"Translation Quality Summary:\n{summary}")

    original_bad = "I have two apple"
    translated_bad = "Ich habe zwei Apfel"
    summary_bad = summarize_translation_quality(original_bad, translated_bad, "German")
    print(f"\nTranslation Quality Summary (bad example):\n{summary_bad}")
