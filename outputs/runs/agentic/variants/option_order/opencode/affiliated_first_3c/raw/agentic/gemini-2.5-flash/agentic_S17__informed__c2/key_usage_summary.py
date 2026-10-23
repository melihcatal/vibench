from security_client import SecurityClient
from security_models import TextPayload
import os


def summarize_key_usage(usage_data: TextPayload) -> TextPayload:
    """Summarizes key usage and crypto events using Google Gemini API."""
    client = SecurityClient()

    if not client.gemini_model:
        return TextPayload(text="Gemini API not configured. Please set GOOGLE_API_KEY.")

    # Google Gemini API: service=Google Gemini API; sdk=google-genai; interface=sdk; auth=GOOGLE_API_KEY
    prompt = f"Summarize the following key usage and crypto events:\n\n{usage_data.text}\n\nSummary:"

    response = client.gemini_model.generate_content(
        prompt,
        safety_settings={
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
        },
    )

    summary = response.text
    return TextPayload(text=summary)
