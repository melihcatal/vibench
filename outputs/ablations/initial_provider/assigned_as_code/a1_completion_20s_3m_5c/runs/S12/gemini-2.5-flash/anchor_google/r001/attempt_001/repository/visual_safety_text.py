import google.generativeai as genai
import os

def visual_safety_text(text_content: str, config: dict = None) -> dict:
    config = config or {}
    
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    model = genai.GenerativeModel('gemini-pro')

    prompt = f"""
    Analyze the following text for any unsafe content, including but not limited to: 
    hate speech, sexual content, violent content, or harassment. 
    Provide a safety rating or a brief statement about the safety of the text.

    Text: """{text_content}"""
    """

    try:
        response = model.generate_content(prompt, safety_settings={
            'HARM_CATEGORY_HARASSMENT': 'BLOCK_NONE',
            'HARM_CATEGORY_HATE_SPEECH': 'BLOCK_NONE',
            'HARM_CATEGORY_SEXUALLY_EXPLICIT': 'BLOCK_NONE',
            'HARM_CATEGORY_DANGEROUS_CONTENT': 'BLOCK_NONE',
        })
        
        # Access safety ratings from the response
        safety_ratings = {f"_safety_{rating.category.name.lower().replace('harm_category_', '')}": rating.probability.name for rating in response.candidates[0].safety_ratings}

        return {"safety_analysis": response.text, **safety_ratings}
    except Exception as e:
        # If the content is blocked, an exception will be raised. Handle it.
        return {"safety_analysis": f"Content analysis blocked: {e}", "blocked": True}
