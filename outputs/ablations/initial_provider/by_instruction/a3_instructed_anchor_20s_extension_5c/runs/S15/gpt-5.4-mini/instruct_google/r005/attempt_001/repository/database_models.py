from dataclasses import dataclass


def normalize_document(data):
    if data is None:
        return {}
    if isinstance(data, dict):
        return dict(data)
    raise TypeError("document data must be a mapping")


@dataclass
class DocumentRequest:
    document_id: str
    data: dict


@dataclass
class DocumentResponse:
    document_id: str
    data: dict
    found: bool = True
