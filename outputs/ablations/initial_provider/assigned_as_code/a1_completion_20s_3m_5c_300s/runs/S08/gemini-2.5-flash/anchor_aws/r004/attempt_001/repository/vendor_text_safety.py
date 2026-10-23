import os
from typing import Dict, Any
import google.generativeai as genai

def moderate_vendor_text_safety(text_to_moderate: str) -> Dict[str, Any]:
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    model = genai.GenerativeModel('gemini-pro') # Using gemini-pro for content analysis

    # The GenerativeModel has built-in safety settings. We can also prompt it for safety analysis.
    safety_prompt = f"""Analyze the following text for any unsafe content (e.g., hate speech, harassment, self-harm, sexual content, dangerous content). Respond with 'clean' if safe, or identify the type of unsafe content if present.
    Text: """{text_to_moderate}"""
    """

    try:
        response = model.generate_content(safety_prompt)
        moderation_result = response.text.strip().lower()
        is_safe = moderation_result == 'clean'
    except Exception as e:
        moderation_result = f"Moderation failed: {e}"
        is_safe = False

    return {"text": text_to_moderate, "is_safe": is_safe, "moderation_result": moderation_result}
