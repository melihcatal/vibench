import google.generativeai as genai
import os
import json
from model_client import get_gemini_client

def extract_json(text: str) -> dict:
    """
    Calls a hosted LLM (Gemini) to extract structured JSON from text.
    """
    client = get_gemini_client()
    model = client.GenerativeModel("gemini-pro")
    
    prompt = f"""Extract information from the following text into a JSON object with 'name', 'age', and 'city' fields.
If a field is not present, use null.

Text: {text}

JSON:
"""
    response = model.generate_content(prompt)
    
    try:
        # Gemini may return markdown-formatted JSON, so we need to clean it.
        json_str = response.text.strip().lstrip("```json").rstrip("```")
        return json.loads(json_str)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        print(f"Raw LLM response: {response.text}")
        return {}

if __name__ == '__main__':
    os.environ["GOOGLE_API_KEY"] = "YOUR_GEMINI_API_KEY" # Replace with your actual key or set it in your environment
    
    sample_text = "John Doe is 30 years old and lives in New York."
    extracted_data = extract_json(sample_text)
    print(f"Original Text: {sample_text}\n")
    print(f"Extracted JSON: {extracted_data}")

    sample_text_2 = "Jane Smith works as a software engineer."
    extracted_data_2 = extract_json(sample_text_2)
    print(f"\nOriginal Text: {sample_text_2}\n")
    print(f"Extracted JSON: {extracted_data_2}")
