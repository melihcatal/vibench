import google.generativeai as genai

def ocr_safety(payload, config=None):
    config = config or {}
    genai.configure(api_key=config["gemini_api_key"])
    model = genai.GenerativeModel('gemini-pro')

    text_to_check = payload["text"]

    # Using the generate_content method and accessing the prompt_feedback for safety ratings
    response = model.generate_content(text_to_check, 
                                      safety_settings=[{"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
                                                       {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
                                                       {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
                                                       {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"}])

    safety_ratings = []
    if hasattr(response, 'prompt_feedback') and response.prompt_feedback.safety_ratings:
        for rating in response.prompt_feedback.safety_ratings:
            safety_ratings.append({"category": str(rating.category).split('_')[-1], "probability": str(rating.probability).split('_')[-1]})

    return {"text": text_to_check, "safety_ratings": safety_ratings}
