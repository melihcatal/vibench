import os
import google.generativeai as genai

# Configure Google Cloud Vertex AI
genai.configure(api_key=os.environ.get("VERTEX_AI_API_KEY"))

def check_text_safety(text: str):
    if not text:
        return {"status": "success", "safe": True, "message": "No text to check."}

    model = genai.GenerativeModel('gemini-pro')

    # The safety settings are applied by default when using generate_content. 
    # The model will block content that violates safety policies.
    # For an explicit check, you might typically send text to a dedicated content moderation API.
    # For demonstration using gemini-pro, we'll rely on its built-in safety features
    # and interpret a blocked response as unsafe. A more robust solution would involve 
    # using a dedicated content moderation service like Google Cloud's Perspective API or similar.
    
    try:
        response = model.generate_content(
            f"Review the following text for safety and harmful content. Respond with 'safe' if it is safe, and 'unsafe' with a brief reason if it contains harmful content.\n\nText: {text}"
        )

        # If the response is blocked due to safety, we consider it unsafe.
        # This is a simplification; a real safety API would provide more granular categories.
        if response._chunks and response._chunks[0].safety_ratings and \
           any(rating.blocked for rating in response._chunks[0].safety_ratings):
            return {"status": "success", "safe": False, "message": "Content potentially unsafe based on safety ratings."}
        
        # Otherwise, we check the model's explicit response for 'unsafe' keyword
        if "unsafe" in response.text.lower():
            return {"status": "success", "safe": False, "message": response.text}
        else:
            return {"status": "success", "safe": True, "message": response.text}

    except Exception as e:
        return {"status": "error", "message": str(e)}
