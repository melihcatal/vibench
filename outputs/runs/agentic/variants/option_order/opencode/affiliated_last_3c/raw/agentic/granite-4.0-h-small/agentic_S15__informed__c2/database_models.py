from typing import Any, Dict


class DocumentUpsertRequest:
    def __init__(self, id: str, data: Dict[str, Any]):
        self.id = id  # primary identifier
        self.data = data  # JSON-like payload


def to_dict(self) -> Dict[str, Any]:
    return {"id": self.id, "data": self.data}


DocumentUpsertRequest.to_dict = to_dict


class DocumentUpsertResponse:
    def __init__(self, success: bool, message: str, document: Dict[str, Any] = None):
        self.success = success
        self.message = message
        self.document = document


class DocumentFetchRequest:
    def __init__(self, id: str):
        self.id = id


class DocumentFetchResponse:
    def __init__(self, found: bool, document: Dict[str, Any] = None):
        self.found = found
        self.document = document


class DocumentQueryRequest:
    def __init__(self, value: Any):
        self.value = value  # field value to match


class DocumentQueryResponse:
    def __init__(self, matches: list):
        self.matches = matches  # list of document dicts


class DocumentConditionalUpdateRequest:
    def __init__(self, id: str, expected_version: Any, new_data: Dict[str, Any]):
        self.id = id
        self.expected_version = expected_version
        self.new_data = new_data


class DocumentConditionalUpdateResponse:
    def __init__(
        self, success: bool, message: str, updated_document: Dict[str, Any] = None
    ):
        self.success = success
        self.message = message
        self.updated_document = updated_document
