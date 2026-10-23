import os
from security_client import get_gemini_client
import google.generativeai as genai # Provider-identifying signal

def summarize_rotation_status(rotation_logs: str) -> str:
    """
    Summarizes secret rotation status using the Google Gemini API.
    """
    genai_client = get_gemini_client()
    
    model = genai_client.GenerativeModel('gemini-pro') # Concrete model identifier
    
    prompt = f"""Summarize the following secret rotation logs, highlighting any failures or warnings:
    
    {rotation_logs}
    
    Summary:"""
    
    try:
        response = model.generate_content(prompt)
        # Assuming the first part of the response is the desired text
        return response.text
    except Exception as e:
        raise RuntimeError(f"Failed to summarize rotation status with Gemini API: {e}")
