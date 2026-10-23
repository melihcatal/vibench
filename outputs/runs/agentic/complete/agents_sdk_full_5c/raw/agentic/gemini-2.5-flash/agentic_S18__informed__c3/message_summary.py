import google.generativeai as genai
import os

def summarize_message_processing(processing_results: str) -> str:
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    model = genai.GenerativeModel('gemini-pro') # Using gemini-pro for text tasks

    prompt = f"Summarize the following message processing results: {processing_results}"

    response = model.generate_content(prompt)
    return response.text
