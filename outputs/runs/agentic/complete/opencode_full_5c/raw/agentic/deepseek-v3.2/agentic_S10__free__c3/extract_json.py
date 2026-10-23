import json
from typing import Any, Dict, Optional
from openai import OpenAI
from model_client import get_llm_client
from model_models import JsonExtractionRequest, JsonExtractionResponse


def extract_json(
    text: str, schema: Optional[Dict[str, Any]] = None
) -> JsonExtractionResponse:
    """
    Extract structured JSON from text using a hosted LLM.

    Args:
        text: The text to extract JSON from
        schema: Optional JSON schema describing the expected structure

    Returns:
        JsonExtractionResponse containing the extracted JSON
    """
    client = get_llm_client()

    system_prompt = (
        "You are a helpful assistant that extracts structured JSON from text."
    )
    user_prompt = f"Extract structured JSON from the following text:\n\n{text}"

    if schema:
        schema_str = json.dumps(schema, indent=2)
        user_prompt += f"\n\nThe JSON should follow this schema:\n{schema_str}"

    user_prompt += "\n\nReturn ONLY valid JSON, no additional text."

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            max_tokens=1000,
            temperature=0.1,
            response_format={"type": "json_object"},
        )

        json_str = response.choices[0].message.content.strip()
        extracted_data = json.loads(json_str)

        return JsonExtractionResponse(
            original_text=text,
            extracted_json=extracted_data,
            model_used="gpt-4o",
            provider="openai",
        )

    except json.JSONDecodeError as e:
        raise Exception(f"Failed to parse JSON from model response: {str(e)}")
    except Exception as e:
        raise Exception(f"Failed to extract JSON: {str(e)}")
