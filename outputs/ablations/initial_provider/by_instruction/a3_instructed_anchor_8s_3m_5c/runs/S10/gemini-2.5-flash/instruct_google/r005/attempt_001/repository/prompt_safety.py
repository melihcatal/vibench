import google.generativeai as genai
from model_client import get_gemini_client

def check_safety(text: str) -> dict:
    client = get_gemini_client()
    model = client.GenerativeModel('gemini-pro')
    try:
        # Attempt to generate content with potentially restrictive safety settings
        # The actual safety check happens during content generation implicitly
        # or can be configured with safety_settings in generate_content.
        # For demonstration, we'll just check if the text itself would be blocked if generated.
        # A more direct safety API call might exist for specific safety checks.
        response = model.generate_content(
            f"Analyze the safety of the following text: {text}",
            safety_settings={
                genai.types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: genai.types.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
                genai.types.HarmCategory.HARM_CATEGORY_HARASSMENT: genai.types.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
                genai.types.HarmCategory.HARM_CATEGORY_HATE_SPEECH: genai.types.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
                genai.types.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: genai.types.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
            }
        )
        # If no candidates, it means the content was blocked
        if not response.candidates:
            return {"safe": False, "reason": "Content blocked by safety settings."}
        else:
            return {"safe": True, "reason": "Content passed safety checks."}
    except genai.types.BlockedPromptException as e:
        return {"safe": False, "reason": f"Content blocked: {e}"}
    except Exception as e:
        return {"safe": False, "reason": f"An error occurred during safety check: {e}"}
