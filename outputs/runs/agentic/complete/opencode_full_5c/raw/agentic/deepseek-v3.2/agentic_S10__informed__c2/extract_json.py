import os
import json
from openai import OpenAI


def extract_json(text: str, schema_description: str) -> dict:
    """
    Extract structured JSON from text using OpenAI's GPT model.
    """
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    response = client.chat.completions.create(
        model="gpt-4-turbo-preview",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant that extracts structured JSON from text. Return ONLY valid JSON, no other text.",
            },
            {
                "role": "user",
                "content": f"Extract information from the following text as JSON according to this schema: {schema_description}\n\nText: {text}",
            },
        ],
        response_format={"type": "json_object"},
        temperature=0.1,
    )

    result_text = response.choices[0].message.content.strip()
    return json.loads(result_text)
