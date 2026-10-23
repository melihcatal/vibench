import google.generativeai as genai
import os

def summarize_translation_quality(payload, config=None):
    config = config or {}
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    model = genai.GenerativeModel('gemini-pro')
    prompt = f"Summarize the potential quality issues in this translation from {payload['source_language']} to {payload['target_language']}:\nSource: {payload['source_text']}\nTranslation: {payload['translated_text']}\nIssues: {payload.get('issues', '')}"
    response = model.generate_content(prompt)
    return {
        "summary": response.text,
        "source_language": payload["source_language"],
        "target_language": payload["target_language"],
    }
