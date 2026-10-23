from dataclasses import dataclass


def normalize_document_id(value):
    if value is None:
        return None
    return str(value)


def normalize_payload(payload):
    if payload is None:
        return {}
    if hasattr(payload, "items"):
        return {str(k): v for k, v in payload.items()}
    return payload


@dataclass
class DocumentResult:
    id: str
    data: dict
    exists: bool = True


@dataclass
class UpdateResult:
    id: str
    data: dict
    updated: bool = True
