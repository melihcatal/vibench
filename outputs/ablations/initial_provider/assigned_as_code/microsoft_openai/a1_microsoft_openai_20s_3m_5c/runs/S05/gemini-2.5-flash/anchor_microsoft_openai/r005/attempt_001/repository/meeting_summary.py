import google.generativeai as genai
import os

def summarize_transcript_chunk(transcript_text: str) -> str:
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

    model = genai.GenerativeModel('gemini-pro')

    prompt = f"Summarize the following meeting transcript chunk:

{transcript_text}

Summary:"

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Error summarizing transcript: {e}")
        return f"[Error summarizing: {e}]"
