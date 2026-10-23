import openai
import json
import os

def extract_json_from_text(text: str) -> dict:
    """
    Calls a hosted LLM (OpenAI GPT-3.5-turbo) to extract structured JSON from text.

    Args:
        text: The input text from which to extract JSON.

    Returns:
        A dictionary representing the extracted JSON.
    """
    openai.api_key = os.environ.get("OPENAI_API_KEY")

    if not openai.api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")

    messages = [
        {"role": "system", "content": "You are a helpful assistant that extracts JSON objects from text."},
        {"role": "user", "content": f"Extract the JSON object from the following text:

{text}

Return only the JSON object."}
    ]

    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",  # Provider-specific model identifier
            messages=messages,
            response_format={"type": "json_object"},
            temperature=0.0
        )
        json_string = response.choices[0].message.content
        return json.loads(json_string)
    except Exception as e:
        print(f"Error extracting JSON: {e}")
        return {}

if __name__ == "__main__":
    example_text = """
    Here is some information about a person:
    {
      "name": "John Doe",
      "age": 30,
      "city": "New York"
    }
    Please process this data.
    """
    extracted_data = extract_json_from_text(example_text)
    print("Extracted JSON:", extracted_data)

    example_text_2 = "No JSON here, just some plain text."
    extracted_data_2 = extract_json_from_text(example_text_2)
    print("Extracted JSON (should be empty):", extracted_data_2)
