import os
import json
from openai import OpenAI


def extract_json(text: str, schema_description: str) -> dict:
    """
    Extract structured JSON from text using OpenAI's GPT model.
    """
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    response = client.chat.completions.create(
        model="gpt-4o-mini",
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

    result = response.choices[0].message.content.strip()
    return json.loads(result)
