import os
import json
import re
from typing import Dict, List, Any, Optional, Union
from datetime import datetime


def extract_structured_fields(
    text: str, field_schema: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Extract structured fields from OCR-normalized document text using OpenAI GPT.

    Args:
        text: OCR-normalized text
        field_schema: Schema defining fields to extract with their types and patterns

    Returns:
        Dictionary of extracted fields
    """
    import openai

    client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY", "your-api-key"))

    schema_description = []
    for field_name, field_info in field_schema.items():
        field_desc = f"- {field_name}: {field_info.get('description', '')}"
        if field_info.get("type"):
            field_desc += f" (type: {field_info['type']})"
        if field_info.get("pattern"):
            field_desc += f" (pattern: {field_info['pattern']})"
        schema_description.append(field_desc)

    schema_text = "\n".join(schema_description)

    prompt = f"""Extract the following fields from the document text below. Return only a JSON object with the field names as keys and extracted values.

Fields to extract:
{schema_text}

Document text:
{text}

Return JSON only:"""

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are a document processing assistant that extracts structured fields from text. Return only valid JSON.",
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.1,
        max_tokens=500,
    )

    result_text = response.choices[0].message.content.strip()

    try:
        result_json = json.loads(result_text)
    except json.JSONDecodeError:
        result_json = {}

    validated_result = {}
    for field_name, field_info in field_schema.items():
        if field_name in result_json:
            value = result_json[field_name]
            validated_result[field_name] = validate_field_value(value, field_info)
        else:
            validated_result[field_name] = None

    return validated_result


def validate_field_value(value: Any, field_info: Dict[str, Any]) -> Any:
    """
    Validate and normalize a field value based on field schema.

    Args:
        value: Extracted value
        field_info: Field schema information

    Returns:
        Validated and normalized value
    """
    if value is None:
        return None

    field_type = field_info.get("type", "string")

    if field_type == "string":
        if isinstance(value, str):
            return value.strip()
        return str(value).strip()

    elif field_type == "number":
        try:
            if isinstance(value, (int, float)):
                return float(value)
            cleaned = re.sub(r"[^\d.-]", "", str(value))
            return float(cleaned) if cleaned else None
        except (ValueError, TypeError):
            return None

    elif field_type == "integer":
        try:
            if isinstance(value, int):
                return value
            cleaned = re.sub(r"[^\d-]", "", str(value))
            return int(cleaned) if cleaned else None
        except (ValueError, TypeError):
            return None

    elif field_type == "date":
        try:
            if isinstance(value, datetime):
                return value.strftime("%Y-%m-%d")

            date_str = str(value).strip()

            date_patterns = [
                r"(\d{1,2})[/-](\d{1,2})[/-](\d{4})",
                r"(\d{4})[/-](\d{1,2})[/-](\d{1,2})",
                r"(\d{1,2})\s+([A-Za-z]+)\s+(\d{4})",
            ]

            for pattern in date_patterns:
                match = re.search(pattern, date_str)
                if match:
                    return date_str

            return date_str
        except Exception:
            return str(value).strip()

    elif field_type == "boolean":
        if isinstance(value, bool):
            return value

        str_value = str(value).lower().strip()
        true_values = ["true", "yes", "y", "1", "t"]
        false_values = ["false", "no", "n", "0", "f"]

        if str_value in true_values:
            return True
        elif str_value in false_values:
            return False
        else:
            return None

    else:
        return str(value).strip()


def extract_fields_with_patterns(text: str, patterns: Dict[str, str]) -> Dict[str, Any]:
    """
    Extract fields using regex patterns.

    Args:
        text: OCR-normalized text
        patterns: Dictionary mapping field names to regex patterns

    Returns:
        Dictionary of extracted fields
    """
    results = {}

    for field_name, pattern in patterns.items():
        match = re.search(pattern, text, re.IGNORECASE | re.MULTILINE)
        if match:
            if match.groups():
                results[field_name] = match.group(1).strip()
            else:
                results[field_name] = match.group(0).strip()
        else:
            results[field_name] = None

    return results


def extract_invoice_fields(text: str) -> Dict[str, Any]:
    """
    Extract common invoice fields from OCR text.

    Args:
        text: Invoice text

    Returns:
        Dictionary of invoice fields
    """
    invoice_schema = {
        "invoice_number": {
            "description": "Invoice number or identifier",
            "type": "string",
        },
        "invoice_date": {"description": "Date of the invoice", "type": "date"},
        "due_date": {"description": "Due date for payment", "type": "date"},
        "vendor_name": {
            "description": "Name of the vendor or seller",
            "type": "string",
        },
        "customer_name": {
            "description": "Name of the customer or buyer",
            "type": "string",
        },
        "total_amount": {"description": "Total amount due", "type": "number"},
        "tax_amount": {"description": "Tax amount", "type": "number"},
        "subtotal": {"description": "Subtotal before tax", "type": "number"},
    }

    return extract_structured_fields(text, invoice_schema)


def extract_receipt_fields(text: str) -> Dict[str, Any]:
    """
    Extract common receipt fields from OCR text.

    Args:
        text: Receipt text

    Returns:
        Dictionary of receipt fields
    """
    receipt_schema = {
        "merchant_name": {
            "description": "Name of the merchant or store",
            "type": "string",
        },
        "transaction_date": {"description": "Date of the transaction", "type": "date"},
        "transaction_time": {
            "description": "Time of the transaction",
            "type": "string",
        },
        "total_amount": {"description": "Total amount paid", "type": "number"},
        "tax_amount": {"description": "Tax amount", "type": "number"},
        "payment_method": {
            "description": "Method of payment (cash, credit card, etc.)",
            "type": "string",
        },
        "items_count": {"description": "Number of items purchased", "type": "integer"},
    }

    return extract_structured_fields(text, receipt_schema)


def extract_contract_fields(text: str) -> Dict[str, Any]:
    """
    Extract common contract fields from OCR text.

    Args:
        text: Contract text

    Returns:
        Dictionary of contract fields
    """
    contract_schema = {
        "contract_title": {"description": "Title of the contract", "type": "string"},
        "effective_date": {
            "description": "Effective date of the contract",
            "type": "date",
        },
        "expiration_date": {
            "description": "Expiration date of the contract",
            "type": "date",
        },
        "parties": {"description": "Names of the parties involved", "type": "string"},
        "contract_value": {
            "description": "Value or amount specified in contract",
            "type": "number",
        },
        "termination_clause": {
            "description": "Presence of termination clause (yes/no)",
            "type": "boolean",
        },
    }

    return extract_structured_fields(text, contract_schema)
