import os
import google.generativeai as genai


def moderate_claims(free_text_claim: str) -> dict:
    google_api_key = os.environ.get("GOOGLE_API_KEY")
    if not google_api_key:
        raise ValueError("Google API Key must be set as an environment variable (GOOGLE_API_KEY).")

    genai.configure(api_key=google_api_key)
    model = genai.GenerativeModel('gemini-pro')

    # Set up safety settings for content moderation
    safety_settings = [
        {
            "category": "HARM_CATEGORY_HARASSMENT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_HATE_SPEECH",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
    ]

    try:
        response = model.generate_content(
            f"Review the following user claim for appropriateness: {free_text_claim}",
            safety_settings=safety_settings
        )
        # If the content is blocked, response.text might be empty
        if not response.text:
            return {"moderation_status": "BLOCKED", "reason": "Content violated safety policies.", "original_claim": free_text_claim}
        return {"moderation_status": "APPROVED", "moderated_content": response.text, "original_claim": free_text_claim}
    except Exception as e:
        # In case of API errors or blocks that raise exceptions
        return {"moderation_status": "ERROR", "reason": str(e), "original_claim": free_text_claim}
