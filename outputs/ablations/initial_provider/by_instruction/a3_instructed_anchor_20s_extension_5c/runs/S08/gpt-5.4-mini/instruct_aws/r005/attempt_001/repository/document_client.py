import os
from dataclasses import dataclass


@dataclass
class DocumentClientConfig:
    aws_region: str
    textract_api_version: str
    openai_api_key: str
    openai_model: str
    aws_dynamodb_table: str


def load_document_client_config() -> DocumentClientConfig:
    return DocumentClientConfig(
        aws_region=os.getenv("AWS_REGION", os.getenv("AWS_DEFAULT_REGION", "us-east-1")),
        textract_api_version=os.getenv("AWS_TEXTRACT_API_VERSION", "2018-06-27"),
        openai_api_key=os.getenv("OPENAI_API_KEY", ""),
        openai_model=os.getenv("OPENAI_MODEL", "gpt-5.4-mini"),
        aws_dynamodb_table=os.getenv("AWS_DYNAMODB_TABLE", "expense-records"),
    )


def normalize_key(text: str) -> str:
    return "".join(ch.lower() if ch.isalnum() else "_" for ch in text).strip("_")


def coerce_confidence(value):
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0
