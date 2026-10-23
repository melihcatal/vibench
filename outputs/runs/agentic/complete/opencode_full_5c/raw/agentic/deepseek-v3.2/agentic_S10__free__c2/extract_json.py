import os
import json
from openai import OpenAI


def extract_json(text: str, schema_description: str) -> dict:
    """
    Extract structured JSON from text using OpenAI's GPT model.
    """
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant that extracts structured data from text. Always respond with valid JSON only.",
            },
            {
                "role": "user",
                "content": f"Extract data from the following text according to this schema: {schema_description}\n\nText: {text}\n\nReturn only valid JSON, no other text.",
            },
        ],
        max_tokens=500,
        temperature=0.1,
        response_format={"type": "json_object"},
    )

    result = response.choices[0].message.content.strip()
    return json.loads(result)
