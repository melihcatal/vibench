import json
from typing import Dict, List, Any
from document_client import get_openai_client


def extract_fields_from_text(text: str, desired_fields: List[str]) -> Dict[str, Any]:
    """
    Extracts structured fields from text using an OpenAI model.
    """
    client = get_openai_client()

    prompt = f"""
    From the following document text, extract the specified fields.
    Return the result as a JSON object. The fields to extract are: {", ".join(desired_fields)}.
    If a field is not present, its value should be null.

    Document Text:
    ---
    {text}
    ---
    """

    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are an expert data extraction assistant.",
            },
            {"role": "user", "content": prompt},
        ],
        response_format={"type": "json_object"},
    )

    try:
        content = response.choices[0].message.content
        if content:
            return json.loads(content)
        return {}
    except (json.JSONDecodeError, IndexError):
        return {}
