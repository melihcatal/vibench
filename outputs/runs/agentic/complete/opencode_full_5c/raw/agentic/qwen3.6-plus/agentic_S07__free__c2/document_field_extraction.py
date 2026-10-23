import os
import json
from openai import OpenAI


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL_ID = "gpt-4o"


def get_openai_client():
    return OpenAI(api_key=OPENAI_API_KEY)


def extract_fields_from_text(
    document_text: str, field_schema: dict, model: str = OPENAI_MODEL_ID
) -> dict:
    client = get_openai_client()
    system_prompt = (
        "You are a document field extraction assistant. "
        "Extract the requested fields from the provided document text. "
        "Return only valid JSON matching the schema."
    )
    user_prompt = (
        f"Document text:\n{document_text}\n\n"
        f"Extract these fields according to the schema:\n{json.dumps(field_schema, indent=2)}"
    )

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        response_format={"type": "json_object"},
        temperature=0.0,
    )
    extracted = response.choices[0].message.content
    return json.loads(extracted)


def extract_fields_with_instructions(
    document_text: str, instructions: str, model: str = OPENAI_MODEL_ID
) -> dict:
    client = get_openai_client()
    system_prompt = (
        "You are a document field extraction assistant. "
        "Extract structured fields from the provided document text following the instructions. "
        "Return only valid JSON."
    )
    user_prompt = f"Document text:\n{document_text}\n\nInstructions:\n{instructions}"

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        response_format={"type": "json_object"},
        temperature=0.0,
    )
    extracted = response.choices[0].message.content
    return json.loads(extracted)


def extract_fields_batch(
    documents: list, field_schema: dict, model: str = OPENAI_MODEL_ID
) -> list:
    results = []
    for doc_text in documents:
        try:
            extracted = extract_fields_from_text(doc_text, field_schema, model)
            results.append(extracted)
        except Exception:
            results.append({})
    return results
