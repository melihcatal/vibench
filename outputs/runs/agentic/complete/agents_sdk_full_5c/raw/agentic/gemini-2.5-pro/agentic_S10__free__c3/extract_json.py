import json
from model_client import get_cohere_client

def extract_json_from_text(text: str) -> dict:
    """
    Extracts a structured JSON object from a given text using Cohere.

    Args:
        text: The text containing the information to extract.

    Returns:
        A dictionary with the extracted data.
    """
    cohere_client = get_cohere_client()

    preamble = """
    Extract the user's name, email, and company from the following text.
    Return the result as a single, valid JSON object with the keys "name", "email", and "company".
    Do not include any other text or formatting.
    """

    # Provider-specific model ID: command-r
    response = cohere_client.chat(
        preamble=preamble,
        message=text,
        model='command-r',
        temperature=0.0
    )

    try:
        # The response text should be a clean JSON string
        json_output = json.loads(response.text)
        return json_output
    except (json.JSONDecodeError, TypeError) as e:
        print(f"Error decoding JSON from model response: {e}")
        return {}
