from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from datetime import datetime


@dataclass
class DocumentUpsertRequest:
    document_id: str
    document: Dict[str, Any]


@dataclass
class DocumentUpsertResponse:
    success: bool
    document_id: str
    old_document: Optional[Dict[str, Any]] = None
    error_message: Optional[str] = None
    message: str = ""


@dataclass
class DocumentFetchRequest:
    document_id: str


@dataclass
class DocumentFetchResponse:
    success: bool
    document_id: str
    document: Optional[Dict[str, Any]] = None
    error_message: Optional[str] = None
    message: str = ""


@dataclass
class DocumentQueryRequest:
    partition_key: Optional[str] = None
    sort_key: Optional[str] = None
    partition_key_name: str = "partition_key"
    sort_key_name: str = "sort_key"
    field_name: Optional[str] = None
    field_value: Optional[Any] = None


@dataclass
class DocumentQueryResponse:
    success: bool
    documents: List[Dict[str, Any]]
    count: int = 0
    error_message: Optional[str] = None
    message: str = ""


@dataclass
class ConditionalUpdateRequest:
    document_id: str
    updates: Dict[str, Any]
    condition_field: Optional[str] = None
    condition_value: Optional[Any] = None
    version_field: Optional[str] = None
    expected_version: int = 0


@dataclass
class ConditionalUpdateResponse:
    success: bool
    document_id: str
    updated_document: Optional[Dict[str, Any]] = None
    error_message: Optional[str] = None
    message: str = ""


@dataclass
class RecordSummaryRequest:
    document: Dict[str, Any]
    fields_to_summarize: List[str]
    max_length: int = 200


@dataclass
class RecordSummaryResponse:
    success: bool
    summary: str
    error_message: Optional[str] = None
    message: str = ""


@dataclass
class SafetyCheckRequest:
    text: str
    language_code: str = "en"


@dataclass
class SafetyCheckResponse:
    success: bool
    is_safe: bool
    unsafe_categories: List[str]
    confidence_scores: Dict[str, float]
    error_message: Optional[str] = None
    message: str = ""


@dataclass
class TranslationRequest:
    text: str
    source_language_code: str = "auto"
    target_language_code: str = "en"


@dataclass
class TranslationResponse:
    success: bool
    translated_text: str
    source_language_code: str
    target_language_code: str
    error_message: Optional[str] = None
    message: str = ""


@dataclass
class ExportArchiveRequest:
    document_id: str
    document: Dict[str, Any]
    format: str = "json"
    bucket_name: Optional[str] = None


@dataclass
class ExportArchiveResponse:
    success: bool
    document_id: str
    s3_key: Optional[str] = None
    s3_url: Optional[str] = None
    error_message: Optional[str] = None
    message: str = ""


def normalize_document(document: Dict[str, Any]) -> Dict[str, Any]:
    """
    Normalize document data types for DynamoDB storage.
    """
    normalized = {}
    for key, value in document.items():
        if isinstance(value, (str, int, float, bool)):
            normalized[key] = value
        elif isinstance(value, dict):
            normalized[key] = value
        elif isinstance(value, list):
            normalized[key] = value
        elif value is None:
            normalized[key] = ""
        else:
            normalized[key] = str(value)
    return normalized


def parse_dynamodb_item(item: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parse DynamoDB item format to Python dictionary.
    """
    import json

    result = {}
    for key, value in item.items():
        if "S" in value:
            try:
                result[key] = json.loads(value["S"])
            except json.JSONDecodeError:
                result[key] = value["S"]
        elif "N" in value:
            try:
                result[key] = int(value["N"])
            except ValueError:
                result[key] = float(value["N"])
        elif "BOOL" in value:
            result[key] = value["BOOL"]
        elif "L" in value:
            result[key] = [parse_dynamodb_item({"item": v})["item"] for v in value["L"]]
        elif "M" in value:
            result[key] = parse_dynamodb_item(value["M"])
        else:
            result[key] = None
    return result
