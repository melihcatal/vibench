import google.generativeai as genai
import os

def record_text_safety(text_content: str):
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    model = genai.GenerativeModel('gemini-pro')

    # When generating content, you can set safety settings to block content that violates your policies.
    # The safety settings are set at the model level and can be configured for each request.
    # Here, we are checking for all safety categories with default thresholds.
    # This is a basic example; for production, you might refine thresholds or handle specific categories.
    try:
        response = model.generate_content(
            text_content,
            safety_settings=[
                {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
            ]
        )
        # If the response is blocked, it will raise an exception or the candidates will be empty.
        if not response._result.candidates:
            return {"status": "unsafe_content_detected", "safety_feedback": response._result.prompt_feedback}
        else:
            return {"status": "safe_content", "safety_feedback": response._result.prompt_feedback}
    except Exception as e:
        # This might catch cases where the prompt itself is blocked before content generation
        return {"status": "error_checking_safety", "details": str(e)}
