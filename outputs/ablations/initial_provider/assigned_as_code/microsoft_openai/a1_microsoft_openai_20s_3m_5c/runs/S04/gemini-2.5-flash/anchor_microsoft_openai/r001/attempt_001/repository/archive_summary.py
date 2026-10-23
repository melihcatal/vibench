import os
import google.generativeai as genai
from speech_models import SummarizationPayload

def archive_summary(payload: SummarizationPayload):
    genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
    if not os.environ.get("GEMINI_API_KEY"):
        raise ValueError("Gemini API key not found. Please set GEMINI_API_KEY environment variable.")

    model = genai.GenerativeModel('gemini-pro')
    prompt = f"Summarize the following text:\n\n{payload.text}"
    response = model.generate_content(prompt)
    
    return {"summary": response.text}
