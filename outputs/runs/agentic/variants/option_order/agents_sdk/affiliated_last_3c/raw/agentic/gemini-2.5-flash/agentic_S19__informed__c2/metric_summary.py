import os
from typing import List, Dict, Any
import google.generativeai as genai

# Configure the Gemini API client
# Ensure GOOGLE_API_KEY environment variable is set
GEMINI_API_KEY = os.environ.get("GOOGLE_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
else:
    print("Warning: GOOGLE_API_KEY environment variable not set. Gemini API calls may fail.")

def summarize_metric_trends(metric_data_description: str) -> str:
    """Summarizes recent metric trends or anomalies using Google Gemini API."""
    if not GEMINI_API_KEY:
        return "Error: Gemini API key not configured."

    model = genai.GenerativeModel('gemini-pro') # Using a concrete model identifier

    prompt = (
        f"Summarize the following metric data description, highlighting any significant trends or anomalies:\n\n"
        f"{metric_data_description}\n\n"
        f"Summary:"
    )

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error calling Gemini API: {e}"
