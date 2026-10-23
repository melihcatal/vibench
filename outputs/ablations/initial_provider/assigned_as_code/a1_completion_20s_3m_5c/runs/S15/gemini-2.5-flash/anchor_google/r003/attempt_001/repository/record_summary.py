import os
import google.generativeai as genai

def record_summary(payload, config=None):
    config = config or {}
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    model = genai.GenerativeModel('gemini-pro')
    
    text_to_summarize = payload["document_content"]
    prompt = f"Summarize the following document: \n\n{text_to_summarize}"
    
    response = model.generate_content(prompt)
    return {"summary": response.text}
