import os
import google.generativeai as genai

def extract_json(text: str, schema: dict) -> dict:
    """
    Calls Google's Generative AI to extract structured JSON from text
    according to a provided schema.
    """
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    model = genai.GenerativeModel("gemini-pro")
    prompt = f"""Extract information from the following text as JSON.
    The JSON should conform to this schema: {schema}

    Text: {text}
    JSON:"""
    response = model.generate_content(prompt)
    # Assuming the model returns valid JSON directly as text
    import json
    return json.loads(response.text)

