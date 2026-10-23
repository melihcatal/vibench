import os
import google.generativeai as genai

def record_text_safety(payload, config=None):
    config = config or {}
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    model = genai.GenerativeModel('gemini-pro')
    
    text_to_check = payload["document_content"]
    prompt = f"Analyze the safety of the following text and identify any unsafe content: \n\n{text_to_check}"
    
    response = model.generate_content(prompt)
    return {"safety_report": response.text}
