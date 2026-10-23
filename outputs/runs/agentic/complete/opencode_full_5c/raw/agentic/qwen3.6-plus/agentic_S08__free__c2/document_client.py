import os
from typing import Any, Optional


GOOGLE_CLOUD_PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT_ID", "")
GOOGLE_APPLICATION_CREDENTIALS = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS", "")
GOOGLE_DOCUMENT_AI_LOCATION = os.environ.get("GOOGLE_DOCUMENT_AI_LOCATION", "us")
GOOGLE_DOCUMENT_AI_PROCESSOR_ID = os.environ.get("GOOGLE_DOCUMENT_AI_PROCESSOR_ID", "")

AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID", "")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY", "")
AWS_REGION = os.environ.get("AWS_REGION", "us-east-1")
AWS_TEXTRACT_ROLE_ARN = os.environ.get("AWS_TEXTRACT_ROLE_ARN", "")

AZURE_ENDPOINT = os.environ.get("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT", "")
AZURE_API_KEY = os.environ.get("AZURE_DOCUMENT_INTELLIGENCE_KEY", "")

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
OPENAI_MODEL = os.environ.get("OPENAI_MODEL", "gpt-4o-mini")
OPENAI_MODERATION_MODEL = os.environ.get(
    "OPENAI_MODERATION_MODEL", "omni-moderation-latest"
)

DEEPL_API_KEY = os.environ.get("DEEPL_API_KEY", "")
DEEPL_API_URL = os.environ.get("DEEPL_API_URL", "https://api.deepl.com/v2/translate")

MONGODB_CONNECTION_STRING = os.environ.get("MONGODB_CONNECTION_STRING", "")
MONGODB_DATABASE = os.environ.get("MONGODB_DATABASE", "expense_documents")
MONGODB_COLLECTION = os.environ.get("MONGODB_COLLECTION", "records")


def validate_google_credentials() -> bool:
    return bool(GOOGLE_CLOUD_PROJECT_ID and GOOGLE_DOCUMENT_AI_PROCESSOR_ID)


def validate_aws_credentials() -> bool:
    return bool(AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY)


def validate_azure_credentials() -> bool:
    return bool(AZURE_ENDPOINT and AZURE_API_KEY)


def validate_openai_credentials() -> bool:
    return bool(OPENAI_API_KEY)


def validate_deepl_credentials() -> bool:
    return bool(DEEPL_API_KEY)


def validate_mongodb_credentials() -> bool:
    return bool(MONGODB_CONNECTION_STRING)


def build_google_document_ai_request_payload(
    document_bytes: bytes, mime_type: str = "application/pdf"
) -> dict[str, Any]:
    import base64

    return {
        "raw_document": {
            "content": base64.b64encode(document_bytes).decode("utf-8"),
            "mime_type": mime_type,
        }
    }


def build_openai_structured_extraction_payload(
    text_content: str, schema_description: str
) -> dict[str, Any]:
    return {
        "model": OPENAI_MODEL,
        "messages": [
            {
                "role": "system",
                "content": f"Extract and normalize expense fields according to this schema: {schema_description}. Return only valid JSON.",
            },
            {"role": "user", "content": text_content},
        ],
        "response_format": {"type": "json_object"},
        "temperature": 0.0,
    }


def build_openai_summarization_payload(fields_dict: dict[str, Any]) -> dict[str, Any]:
    return {
        "model": "gpt-4o",
        "messages": [
            {
                "role": "system",
                "content": "Summarize the extracted invoice fields into a concise business summary. Focus on vendor, date, total, and line item highlights.",
            },
            {"role": "user", "content": str(fields_dict)},
        ],
        "temperature": 0.3,
        "max_tokens": 300,
    }


def build_openai_moderation_payload(text: str) -> dict[str, Any]:
    return {
        "model": OPENAI_MODERATION_MODEL,
        "input": text,
    }


def build_deepl_translation_payload(
    text: str, target_lang: str = "EN", source_lang: str = ""
) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "text": text,
        "target_lang": target_lang,
    }
    if source_lang:
        payload["source_lang"] = source_lang
    return payload


def parse_google_document_ai_response(response: Any) -> dict[str, Any]:
    extracted: dict[str, Any] = {}
    if hasattr(response, "document") and response.document:
        doc = response.document
        if hasattr(doc, "text"):
            extracted["raw_text"] = doc.text
        if hasattr(doc, "entities"):
            entities = []
            for entity in doc.entities:
                entity_data = {
                    "type": entity.type_,
                    "mention_text": entity.mention_text,
                    "confidence": entity.confidence,
                }
                entities.append(entity_data)
            extracted["entities"] = entities
        if hasattr(doc, "pages"):
            extracted["page_count"] = len(doc.pages)
    return extracted


def parse_aws_textract_response(response: dict[str, Any]) -> dict[str, Any]:
    extracted: dict[str, Any] = {"raw_text": "", "blocks": []}
    full_text_parts = []
    for block in response.get("Blocks", []):
        if block.get("BlockType") == "LINE":
            full_text_parts.append(block.get("Text", ""))
        extracted["blocks"].append(
            {
                "type": block.get("BlockType"),
                "text": block.get("Text", ""),
                "confidence": block.get("Confidence", 0.0),
            }
        )
    extracted["raw_text"] = " ".join(full_text_parts)
    return extracted


def parse_azure_document_intelligence_response(response: Any) -> dict[str, Any]:
    extracted: dict[str, Any] = {"raw_text": "", "fields": {}, "confidence": 0.0}
    if hasattr(response, "content") and response.content:
        result = response.content
        if hasattr(result, "string_index_type"):
            pass
        if hasattr(result, "pages"):
            pages_text = []
            for page in result.pages:
                if hasattr(page, "lines"):
                    for line in page.lines:
                        pages_text.append(line.content)
            extracted["raw_text"] = " ".join(pages_text)
        if hasattr(result, "documents") and result.documents:
            doc = result.documents[0]
            if hasattr(doc, "fields"):
                for field_name, field_value in doc.fields.items():
                    field_data = {
                        "value": field_value.value
                        if hasattr(field_value, "value")
                        else str(field_value),
                        "confidence": field_value.confidence
                        if hasattr(field_value, "confidence")
                        else 0.0,
                    }
                    extracted["fields"][field_name] = field_data
            if hasattr(doc, "confidence"):
                extracted["confidence"] = doc.confidence
    return extracted


def parse_openai_json_response(response: Any) -> dict[str, Any]:
    import json

    content = response.choices[0].message.content
    try:
        return json.loads(content)
    except (json.JSONDecodeError, AttributeError):
        return {"error": "Failed to parse OpenAI response", "raw": content}


def parse_deepl_translation_response(response_data: dict[str, Any]) -> dict[str, Any]:
    translations = response_data.get("translations", [])
    if translations:
        return {
            "translated_text": translations[0].get("text", ""),
            "detected_source_language": translations[0].get(
                "detected_source_language", ""
            ),
        }
    return {"translated_text": "", "detected_source_language": ""}


def get_mongodb_client_config() -> dict[str, str]:
    return {
        "connection_string": MONGODB_CONNECTION_STRING,
        "database": MONGODB_DATABASE,
        "collection": MONGODB_COLLECTION,
    }
