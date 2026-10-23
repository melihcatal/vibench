from typing import Dict, Any, Optional, List
import os
import json
import openai
from document_models import FieldExtractionRequest, FieldExtractionResponse


OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
OPENAI_API_BASE = os.environ.get("OPENAI_API_BASE", "https://api.openai.com/v1")
OPENAI_EXTRACTION_MODEL = "gpt-4o"


def extract_structured_fields(
    text: str,
    schema: Dict[str, Any],
    model: str = OPENAI_EXTRACTION_MODEL,
    temperature: float = 0.0,
) -> FieldExtractionResponse:
    client = openai.OpenAI(api_key=OPENAI_API_KEY, base_url=OPENAI_API_BASE)
    system_prompt = (
        "You are a document field extraction assistant. "
        "Extract structured fields from the provided document text according to the JSON schema. "
        "Return only valid JSON matching the schema. Do not include any explanations."
    )
    schema_str = json.dumps(schema, indent=2)
    user_prompt = (
        f"Extract the following fields from this document text:\n\n"
        f"Document text:\n{text}\n\n"
        f"Required JSON schema:\n{schema_str}"
    )
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=temperature,
        response_format={"type": "json_object"},
    )
    extracted_json = json.loads(response.choices[0].message.content)
    confidence = 1.0
    if response.usage:
        total_tokens = response.usage.total_tokens
        if total_tokens > 500:
            confidence = 0.8
    return FieldExtractionResponse(
        extracted_fields=extracted_json,
        confidence=confidence,
        raw_response={
            "model": model,
            "usage": {
                "prompt_tokens": response.usage.prompt_tokens,
                "completion_tokens": response.usage.completion_tokens,
                "total_tokens": response.usage.total_tokens,
            }
            if response.usage
            else {},
        },
    )


def extract_fields_with_validation(
    text: str,
    schema: Dict[str, Any],
    model: str = OPENAI_EXTRACTION_MODEL,
    max_retries: int = 2,
) -> FieldExtractionResponse:
    client = openai.OpenAI(api_key=OPENAI_API_KEY, base_url=OPENAI_API_BASE)
    system_prompt = (
        "You are a document field extraction assistant. "
        "Extract structured fields from the provided document text according to the JSON schema. "
        "Return only valid JSON matching the schema. Do not include any explanations."
    )
    schema_str = json.dumps(schema, indent=2)
    user_prompt = (
        f"Extract the following fields from this document text:\n\n"
        f"Document text:\n{text}\n\n"
        f"Required JSON schema:\n{schema_str}"
    )
    for attempt in range(max_retries + 1):
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.0,
            response_format={"type": "json_object"},
        )
        try:
            extracted_json = json.loads(response.choices[0].message.content)
            return FieldExtractionResponse(
                extracted_fields=extracted_json,
                confidence=1.0 - (attempt * 0.1),
                raw_response={
                    "model": model,
                    "usage": {
                        "prompt_tokens": response.usage.prompt_tokens,
                        "completion_tokens": response.usage.completion_tokens,
                        "total_tokens": response.usage.total_tokens,
                    }
                    if response.usage
                    else {},
                },
            )
        except (json.JSONDecodeError, KeyError):
            if attempt == max_retries:
                raise
            user_prompt += (
                "\n\nThe previous response was not valid JSON. Please try again."
            )
    return FieldExtractionResponse(extracted_fields={}, confidence=0.0)


def extract_fields_batch(
    texts: List[str],
    schema: Dict[str, Any],
    model: str = OPENAI_EXTRACTION_MODEL,
) -> List[FieldExtractionResponse]:
    responses = []
    for text in texts:
        resp = extract_structured_fields(text, schema, model=model)
        responses.append(resp)
    return responses
