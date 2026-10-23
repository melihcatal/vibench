import os
import google.generativeai as genai

def redact_unsafe_text(text: str, safety_threshold: str = "BLOCK_LOW_AND_ABOVE") -> str:
    """
    Redacts unsafe text by checking against Google Generative AI's safety settings.
    If the text is deemed unsafe based on the configured threshold, it returns a redacted string.
    Otherwise, it returns the original text.
    """
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

    model = genai.GenerativeModel('gemini-pro')

    threshold_enum_map = {
        "BLOCK_NONE": genai.types.HarmBlockThreshold.BLOCK_NONE,
        "BLOCK_FEW": genai.types.HarmBlockThreshold.BLOCK_FEW,
        "BLOCK_SOME": genai.types.HarmBlockThreshold.BLOCK_SOME,
        "BLOCK_LOW_AND_ABOVE": genai.types.HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
    }
    configured_threshold = threshold_enum_map.get(safety_threshold, genai.types.HarmBlockThreshold.BLOCK_LOW_AND_ABOVE)

    safety_settings = [
        {"category": genai.types.HarmCategory.HARM_CATEGORY_HARASSMENT, "threshold": configured_threshold},
        {"category": genai.types.HarmCategory.HARM_CATEGORY_HATE_SPEECH, "threshold": configured_threshold},
        {"category": genai.types.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT, "threshold": configured_threshold},
        {"category": genai.types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT, "threshold": configured_threshold},
    ]

    try:
        response = model.generate_content(
            text,
            safety_settings=safety_settings
        )

        # If the response has no candidates, it means the content was blocked due to safety.
        if not response.candidates:
            return "[REDACTED]"
        else:
            return text

    except Exception:
        # If an error occurs during API call (e.g., content violates even BLOCK_NONE or other API errors),
        # we treat it as unsafe to be cautious.
        return "[REDACTED - Processing Error]"
