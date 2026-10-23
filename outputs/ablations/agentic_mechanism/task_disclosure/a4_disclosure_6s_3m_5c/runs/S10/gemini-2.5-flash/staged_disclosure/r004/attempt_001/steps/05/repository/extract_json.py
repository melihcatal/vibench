import google.generativeai as genai
import os
import json

def extract_json_from_text(text: str) -> dict:
    """
    Calls a hosted LLM (Google Gemini) to extract structured JSON from text.
    """
    try:
        genai.configure(api_key=os.environ["GEMINI_API_KEY"])
    except KeyError:
        raise ValueError("GEMINI_API_KEY environment variable not set.")

    model = genai.GenerativeModel('gemini-pro')

    prompt = f"""
    Extract any structured JSON object from the following text.
    If no JSON object is found, return an empty JSON object {{}}.

    Text:
    """
    {text}
    """

    Please return only the JSON object, nothing else.
    """

    response = model.generate_content(prompt)
    
    # Assuming the model's response directly contains the JSON string
    try:
        json_string = response.text.strip()
        if json_string.startswith("```json") and json_string.endswith("```"):
            json_string = json_string[7:-3].strip()
        
        # Attempt to load the JSON. If it fails, return empty dict.
        return json.loads(json_string)
    except json.JSONDecodeError:
        print(f"Warning: Could not decode JSON from response: {response.text}")
        return {}
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return {}

if __name__ == "__main__":
    # Example usage
    os.environ["GEMINI_API_KEY"] = "YOUR_GEMINI_API_KEY" # Replace with your actual API key

    text_with_json = "Here is some data: {"name": "Alice", "age": 30, "city": "New York"}. And some more text."
    extracted_data = extract_json_from_text(text_with_json)
    print("Extracted JSON:", extracted_data)

    text_without_json = "This text does not contain any JSON data."
    extracted_data_2 = extract_json_from_text(text_without_json)
    print("Extracted JSON (no JSON):", extracted_data_2)

    text_with_invalid_json = "This text has some malformed json: {name: 'Bob', age: 25}."
    extracted_data_3 = extract_json_from_text(text_with_invalid_json)
    print("Extracted JSON (invalid JSON):", extracted_data_3)
