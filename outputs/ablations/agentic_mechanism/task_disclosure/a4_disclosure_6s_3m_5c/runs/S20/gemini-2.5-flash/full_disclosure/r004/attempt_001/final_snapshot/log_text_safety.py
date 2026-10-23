import vertexai
from vertexai.preview.generative_models import GenerativeModel, HarmCategory, SafetySetting

def check_safety(log_message: str):
    """
    Checks the given log message for unsafe content using Google Vertex AI.

    Args:
        log_message: The text of the log message to check.

    Returns:
        A dictionary containing the safety check results.
    """
    model = GenerativeModel("gemini-pro")

    # Configure safety settings to block harmful content
    safety_settings = [
        SafetySetting(category=HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT, threshold=SafetySetting.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE),
        SafetySetting(category=HarmCategory.HARM_CATEGORY_HARASSMENT, threshold=SafetySetting.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE),
        SafetySetting(category=HarmCategory.HARM_CATEGORY_HATE_SPEECH, threshold=SafetySetting.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE),
        SafetySetting(category=HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT, threshold=SafetySetting.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE),
    ]

    try:
        response = model.generate_content(
            log_message,
            safety_settings=safety_settings
        )
        # If the response is blocked, it will raise an exception or have empty parts
        # For a more detailed safety report, one might need to access specific attributes
        # which are not directly exposed in generate_content for safety reasons in some versions.
        # This simplified version checks if content generation was successful.
        return {"is_safe": True, "details": "Content generation successful, no immediate blocks."}
    except Exception as e:
        # A common way for Vertex AI to indicate unsafe content is by blocking generation
        return {"is_safe": False, "details": f"Content blocked or error: {e}"}

