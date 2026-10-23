import os
import google.generativeai as genai

def check_safety(text_payload: str) -> dict:
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    model = genai.GenerativeModel("gemini-pro")

    # Using generate_content for safety check can be a bit indirect.
    # A more direct approach for content moderation would be specific moderation APIs if available.
    # For this exercise, we will prompt gemini-pro to evaluate safety.
    prompt = f"Analyze the following text for unsafe content (e.g., hate speech, violence, sexual content, harmful content). Respond with 'SAFE' or 'UNSAFE' and provide a brief reason if UNSAFE:\n\n{text_payload}"
    
    response = model.generate_content(prompt)
    safety_analysis = response.text

    # Parse the response to determine a simple safety status
    if "UNSAFE" in safety_analysis.upper():
        return {"is_safe": False, "reason": safety_analysis}
    else:
        return {"is_safe": True, "reason": safety_analysis}
