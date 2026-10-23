from typing import Dict, List, Optional
import google.generativeai as genai
from google.generativeai.types import ContentType


def quality_summary(
    source_texts: List[str],
    translated_texts: List[str],
    source_lang: str,
    target_lang: str,
) -> Dict[str, List[str]]:
    """
    Summarizes translation quality issues using Gemini API.
    """
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    model = genai.GenerativeModel(model_name="gemini-1.5-flash")

    issues = {}
    for i, (source, translated) in enumerate(zip(source_texts, translated_texts)):
        prompt = (
            f"Analyze the following translation from {source_lang} to {target_lang}. "
            f"Identify any quality issues such as mistranslations, omissions, or inaccuracies. "
            f"Provide a brief summary of issues found or 'None' if no issues.\n\n"
            f"Source: {source}\n"
            f"Translation: {translated}\n"
        )
        response = model.generate_content(prompt)
        issues[f"text_{i}"] = [response.text.strip()]

    return issues
