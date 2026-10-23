import json
import os
from openai import OpenAI
from model_client import get_client
from model_models import ExtractRequest, ExtractResponse


def extract_json(text: str, schema_description: str) -> dict:
    """Extract structured JSON from text using a hosted LLM."""
    client = get_client()

    prompt = f"""Extract structured data from the following text according to this schema: {schema_description}

Text to extract from:
{text}

Return ONLY valid JSON matching the schema description. Do not include any explanatory text."""

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": "You are a JSON extraction assistant. Always return valid JSON.",
                },
                {"role": "user", "content": prompt},
            ],
            response_format={"type": "json_object"},
            temperature=0.1,
            max_tokens=1000,
        )

        json_str = response.choices[0].message.content.strip()
        return json.loads(json_str)
    except json.JSONDecodeError as e:
        raise Exception(f"Failed to parse JSON response: {str(e)}")
    except Exception as e:
        raise Exception(f"Failed to extract JSON: {str(e)}")
