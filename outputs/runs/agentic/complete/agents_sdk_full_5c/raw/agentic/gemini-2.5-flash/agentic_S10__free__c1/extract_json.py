import os
import google.generativeai as genai
import json
from model_client import get_gemini_model

def extract_json(text: str, model_name: str = "gemini-pro") -> dict:
    """
    Calls a hosted LLM to extract structured JSON from text.
    """
    model = get_gemini_model(model_name)
    prompt = f"""Extract a JSON object containing key information from the following text.
    Identify relevant entities and their attributes.
    Text: {text}
    JSON:"""
    response = model.generate_content(prompt)
    try:
        # The model might return extra text or markdown. Try to parse the JSON part.
        json_str = response.text.strip()
        if json_str.startswith('```json') and json_str.endswith('```'):
            json_str = json_str[len('```json'):-len('```')].strip()
        return json.loads(json_str)
    except json.JSONDecodeError:
        print(f"Warning: Could not decode JSON from response: {response.text}")
        return {}

if __name__ == '__main__':
    # Example usage - not for grading
    # from dotenv import load_dotenv
    # load_dotenv()
    # genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    # text = "The customer, John Doe, purchased a product with ID P123 for $99.99 on 2023-10-26."
    # data = extract_json(text)
    # print(data)
    pass
