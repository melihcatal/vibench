import os
import google.generativeai as genai
from typing import List, Dict, Any

def summarize_moderation_decisions(decisions: List[Dict[str, Any]]):
    """
    Summarize moderation decisions using the Google Gemini API.
    """
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")
    
    genai.configure(api_key=api_key)

    model = genai.GenerativeModel('gemini-pro')

    prompt = f"""Summarize the following moderation decisions.
    Focus on key patterns, common issues, and any urgent flags.

    Moderation Decisions:
    {decisions}

    Summary:
    """

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Error summarizing moderation decisions with Gemini API: {e}")
        return None
