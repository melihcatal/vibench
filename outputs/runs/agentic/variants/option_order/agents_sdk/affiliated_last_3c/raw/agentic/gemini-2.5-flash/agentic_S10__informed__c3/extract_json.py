import google.generativeai as genai
import os
import json

def extract_json(text: str, schema: dict) -> dict:
    """
    Calls a hosted LLM (Google Gemini) to extract structured JSON from text.
    """
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    model = genai.GenerativeModel("gemini-pro")
    prompt = f"Extract information from the following text as a JSON object matching this schema:\n\nSchema: {json.dumps(schema, indent=2)}\n\nText: {text}\n\nJSON:"
    response = model.generate_content(prompt)
    try:
        return json.loads(response.text)
    except json.JSONDecodeError:
        return {}
