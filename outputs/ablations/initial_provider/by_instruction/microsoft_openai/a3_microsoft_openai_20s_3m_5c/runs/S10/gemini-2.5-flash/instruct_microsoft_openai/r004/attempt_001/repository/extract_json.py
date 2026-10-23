import os
import json
from openai import OpenAI

def extract_json(text: str, schema: dict) -> dict:
    """
    Calls a hosted LLM (OpenAI) to extract structured JSON from text based on a provided schema.
    """
    client = OpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),
        base_url=os.getenv("OPENAI_API_BASE", "https://api.openai.com/v1")
    )

    response = client.chat.completions.create(
        model="gpt-4o", # Using a concrete model identifier
        messages=[
            {"role": "system", "content": "You are an AI assistant that extracts information from text and returns it as a JSON object. The JSON should conform to the provided schema."},
            {"role": "user", "content": f"Extract information from the following text into a JSON object conforming to this schema: {json.dumps(schema)}. Text: {text}"}
        ],
        response_format={ "type": "json_object" }
    )
    return json.loads(response.choices[0].message.content)