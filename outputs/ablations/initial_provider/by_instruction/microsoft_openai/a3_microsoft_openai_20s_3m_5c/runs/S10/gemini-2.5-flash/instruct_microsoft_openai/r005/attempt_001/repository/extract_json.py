import os
from openai import OpenAI
import json

def extract_json(text: str, json_schema: dict) -> dict:
    """
    Extracts structured JSON from the given text using a hosted OpenAI LLM.
    """
    client = OpenAI(
        api_key=os.environ.get("OPENAI_API_KEY"),
        organization=os.environ.get("OPENAI_ORGANIZATION"),
    )

    # A system message to guide the model to output valid JSON
    system_message = (
        "You are a helpful assistant designed to output JSON. "
        "Extract information from the user's input based on the provided JSON schema."
    )

    # Include the schema in the prompt to help the model structure its output
    user_message = (
        f"Extract information from the following text into JSON format "
        f"according to this schema: {json.dumps(json_schema)}.\n\nText: {text}"
    )

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # Or another suitable OpenAI model
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message}
        ],
        response_format={"type": "json_object"}
    )
    try:
        return json.loads(response.choices[0].message.content.strip())
    except json.JSONDecodeError:
        # Handle cases where the LLM might not return perfect JSON
        print("Warning: LLM did not return valid JSON. Attempting to parse.")
        return {}
