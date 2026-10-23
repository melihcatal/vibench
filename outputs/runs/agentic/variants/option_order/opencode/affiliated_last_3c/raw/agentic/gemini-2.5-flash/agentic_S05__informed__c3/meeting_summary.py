import os
import google.generativeai as genai

def summarize_transcript_chunk(text: str) -> str:
    # GOOGLE_API_KEY environment variable is expected to be set
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

    model = genai.GenerativeModel('gemini-pro')

    prompt = f"Summarize the following meeting transcript chunk:

{text}

Summary:"

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error summarizing: {e}"
