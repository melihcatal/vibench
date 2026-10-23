import os
import google.generativeai as genai
from storage_models import SummaryResult

def summarize_asset_content(text_content: str) -> SummaryResult:
    """
    Summarizes the provided text content using the Google Gemini API.
    """
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")
    
    genai.configure(api_key=api_key)
    
    # Using a specific Gemini model for the task
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    prompt = f"Please provide a concise summary of the following text:\n\n{text_content}"
    
    response = model.generate_content(prompt)
    
    summary = response.text
    
    print(f"Generated Summary: {summary}")
    
    return SummaryResult(source_text=text_content, summary_text=summary)
