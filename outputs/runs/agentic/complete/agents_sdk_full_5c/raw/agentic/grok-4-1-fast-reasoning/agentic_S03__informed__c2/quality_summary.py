import google.generativeai as genai
import os

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')

def quality_summary(original: str, translation: str) -> str:
    """
    Summarize translation quality issues using Google Gemini.
    """
    prompt = f"""
    Analyze the following translation for quality issues, fluency, accuracy, and suggest improvements.
    
    Original: {original}
    Translation: {translation}
    
    Provide a concise summary of issues.
    """
    response = model.generate_content(prompt)
    return response.text