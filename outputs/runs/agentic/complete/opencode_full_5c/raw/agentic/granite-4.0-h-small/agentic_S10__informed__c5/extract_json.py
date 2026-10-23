import json
import google.genai
from model_client import get_model_client


def extract_json(prompt, max_tokens=300):
    """Extracts structured JSON data from input text using Google Gemini API.

    Args:
        prompt (str): Text containing the data to extract.
        max_tokens (int): Maximum tokens for the model response.

    Returns:
        dict: Parsed JSON object.
    """
    client = get_model_client("gemini")
    response = client.generate_content(
        prompt,
        generation_params={
            "temperature": 0.0,
            "max_output_tokens": max_tokens,
            "response_mime_type": "application/json",
        },
    )
    try:
        return json.loads(response.text)
    except json.JSONDecodeError as e:
        raise ValueError("Generated text is not valid JSON") from e
