import os
import google.generativeai as genai

def summarize_record(text_content: str, model_id: str = 'gemini-pro') -> dict:
    api_key = os.environ.get('GOOGLE_API_KEY')
    if not api_key:
        return {"status": "error", "message": "GOOGLE_API_KEY environment variable not set."}

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(model_id)

    prompt = f"Summarize the following text concisely:\n\n{text_content}"

    try:
        response = model.generate_content(prompt)
        summary = response.text
        return {"status": "success", "summary": summary}
    except Exception as e:
        return {"status": "error", "message": str(e)}
