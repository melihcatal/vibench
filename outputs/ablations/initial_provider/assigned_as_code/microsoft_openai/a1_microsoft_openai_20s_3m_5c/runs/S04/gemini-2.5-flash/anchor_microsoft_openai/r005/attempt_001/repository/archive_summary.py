import os
import google.generativeai as genai


def archive_summary(transcript_text, config=None):
    config = config or {}
    genai.configure(api_key=config.get('api_key') or os.environ.get('GEMINI_API_KEY'))

    model = genai.GenerativeModel('gemini-pro')

    prompt = f"Summarize the following transcript:

{transcript_text}

Summary:"
    response = model.generate_content(prompt)

    return {"summary": response.text, "provider": "Google Cloud Generative AI (gemini-pro)"}
