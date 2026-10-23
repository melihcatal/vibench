import os
import google.generativeai as genai

def summarize_transcription_results(transcript_text: str, model_name: str = "gemini-pro") -> str:
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("Google API Key not provided and GOOGLE_API_KEY environment variable not set.")
    
    genai.configure(api_key=api_key)

    model = genai.GenerativeModel(model_name)
    prompt = f"Summarize the following transcript:\n\n{transcript_text}\n\nSummary:"
    
    response = model.generate_content(prompt)
    return response.text
