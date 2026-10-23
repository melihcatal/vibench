import google.generativeai as genai

def secret_label_safety_check(text_to_check: str, config: dict) -> dict:
    genai.configure(api_key=config.get("GEMINI_API_KEY"))
    model = genai.GenerativeModel('gemini-pro')
    
    # The generative model inherently has safety settings applied during content generation.
    # To explicitly check for safety attributes, one would typically configure safety_settings
    # when making a generate_content call or analyze a text specifically for safety categories.
    # For this example, we'll demonstrate a check by asking the model to identify unsafe content if any.
    # A more robust solution might involve a dedicated content moderation API if available.

    prompt = f"Analyze the following text for any potentially unsafe content, such as hate speech, sexual content, harassment, or dangerous content. If unsafe, describe why. Otherwise, state it is safe:\n\n\'''{text_to_check}'''"
    
    response = model.generate_content(prompt)
    return {"safety_analysis": response.text}
