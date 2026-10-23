import json
import os
from openai import OpenAI
from model_client import get_client
from model_models import ExtractRequest, ExtractResponse


def extract_json(text: str, schema: dict) -> dict:
    """
    Extract structured JSON from text using a hosted LLM.
    """
    client = get_client()

    schema_str = json.dumps(schema, indent=2)
    prompt = f"""Extract structured data from the following text according to this JSON schema:

Schema:
{schema_str}

Text:
{text}

Return ONLY valid JSON that matches the schema. Do not include any explanations or additional text."""

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": "You are a precise data extraction assistant that outputs only valid JSON.",
                },
                {"role": "user", "content": prompt},
            ],
            response_format={"type": "json_object"},
            temperature=0.1,
            max_tokens=1000,
        )

        result_text = response.choices[0].message.content.strip()
        extracted_data = json.loads(result_text)
        return extracted_data
    except json.JSONDecodeError as e:
        raise Exception(f"Failed to parse JSON response: {str(e)}")
    except Exception as e:
        raise Exception(f"Failed to extract JSON: {str(e)}")
