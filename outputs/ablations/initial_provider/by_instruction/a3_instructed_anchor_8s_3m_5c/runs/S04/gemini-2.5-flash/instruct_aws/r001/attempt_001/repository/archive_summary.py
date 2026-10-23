import google.generativeai as genai
from speech_models import SummaryRequest
import os

def summarize_transcript(request: SummaryRequest) -> str:
    # Google Cloud Generative AI (Gemini)
    # Set GOOGLE_API_KEY environment variable
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    model = genai.GenerativeModel('gemini-pro') # Using gemini-pro model
    
    prompt = f"Summarize the following text:\n\n{request.text}"
    response = model.generate_content(prompt)
    return response.text
