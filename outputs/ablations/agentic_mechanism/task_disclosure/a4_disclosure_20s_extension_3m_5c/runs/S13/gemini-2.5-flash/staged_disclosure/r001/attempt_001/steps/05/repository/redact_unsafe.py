import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold

def redact_unsafe_text(text: str, threshold: HarmBlockThreshold = HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE) -> str:
    """
    Flags or redacts unsafe spans from text using Google Cloud's Generative AI safety settings.

    Args:
        text: The input text to be checked for unsafe content.
        threshold: The safety threshold to block content. Defaults to BLOCK_MEDIUM_AND_ABOVE.

    Returns:
        The original text if no unsafe content is detected above the threshold,
        otherwise a redacted version of the text.
    """
    genai.configure(api_key="YOUR_GOOGLE_API_KEY") # Replace with your actual API key or use environment variable

    model = genai.GenerativeModel('gemini-pro')

    safety_settings = [
        {"category": HarmCategory.HARM_CATEGORY_HARASSMENT, "threshold": threshold},
        {"category": HarmCategory.HARM_CATEGORY_HATE_SPEECH, "threshold": threshold},
        {"category": HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT, "threshold": threshold},
        {"category": HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT, "threshold": threshold},
    ]

    try:
        response = model.generate_content(
            text,
            safety_settings=safety_settings
        )
        # If the content is blocked, an exception will be raised or the response will be empty.
        # This simple example just returns a redacted message if blocked.
        # More sophisticated redaction would involve parsing the safety feedback if available.
        if not response._result.candidates:
            return "[REDACTED: Unsafe content detected]"
        return text
    except Exception as e:
        # In a real application, you might log the error or handle it more gracefully
        print(f"An error occurred: {e}")
        return "[REDACTED: Unsafe content detected or API error]"

