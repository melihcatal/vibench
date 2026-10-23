import os
import google.generativeai as genai

def summarize_moderation_decision(moderation_result: dict, original_text: str) -> str:
    genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
    model = genai.GenerativeModel('gemini-pro')

    prompt = f"""Summarize the moderation decision for the following text. 
Text: """{original_text}"""
Moderation Result: {moderation_result}

Provide a concise summary of why the text was flagged or not flagged, including the categories and their severities. """

    response = model.generate_content(prompt)
    return response.text
