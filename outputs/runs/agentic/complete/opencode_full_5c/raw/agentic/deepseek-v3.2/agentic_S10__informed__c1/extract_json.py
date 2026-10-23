import json
import os
from model_client import get_openai_client


def extract_json_from_text(text: str, schema_description: str) -> dict:
    """Extract structured JSON from text using OpenAI GPT model."""
    client = get_openai_client()

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant that extracts structured JSON from text. Always return valid JSON.",
            },
            {
                "role": "user",
                "content": f"Extract information from the following text as JSON with this schema: {schema_description}\n\nText: {text}\n\nReturn only the JSON object, no other text.",
            },
        ],
        response_format={"type": "json_object"},
        temperature=0.1,
    )

    result_text = response.choices[0].message.content.strip()
    return json.loads(result_text)
