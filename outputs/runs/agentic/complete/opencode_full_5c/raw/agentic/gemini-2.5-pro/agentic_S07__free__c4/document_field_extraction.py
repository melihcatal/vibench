import os
import json
import openai


def extract_fields_from_text(document_text: str, fields: list[str]) -> dict:
    """
    Extracts structured fields from text using an OpenAI model.

    Args:
        document_text: The text extracted from a document.
        fields: A list of field names to extract.

    Returns:
        A dictionary containing the extracted fields.
    """
    # Provider-specific client class
    client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    prompt = f"""
    From the following document text, extract the specified fields.
    Return the result as a JSON object with the field names as keys.
    If a field is not found, its value should be null.

    Fields to extract: {", ".join(fields)}

    Document text:
    ---
    {document_text}
    ---
    """

    # Provider-specific model ID
    model_name = "gpt-4o-mini"

    response = client.chat.completions.create(
        model=model_name,
        messages=[
            {
                "role": "system",
                "content": "You are an expert document field extraction assistant.",
            },
            {"role": "user", "content": prompt},
        ],
        response_format={"type": "json_object"},
        temperature=0.0,
    )

    try:
        content = response.choices[0].message.content
        return json.loads(content)
    except (json.JSONDecodeError, IndexError):
        return {}
