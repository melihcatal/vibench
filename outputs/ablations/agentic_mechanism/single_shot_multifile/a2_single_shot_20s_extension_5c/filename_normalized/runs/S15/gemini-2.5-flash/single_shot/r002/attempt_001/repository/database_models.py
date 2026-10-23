from typing import Dict, Any, Optional

class Document:
    def __init__(self, id: str, data: Dict[str, Any]):
        self.id = id
        self.data = data

    def to_dict(self) -> Dict[str, Any]:
        return {"id": self.id, **self.data}

    @staticmethod
    def from_dict(doc_data: Dict[str, Any]) -> Optional['Document']:
        if 'id' in doc_data:
            doc_id = doc_data.pop('id')
            return Document(id=doc_id, data=doc_data)
        return None

class QueryParams:
    def __init__(self, field_name: str, field_value: str, index_name: Optional[str] = None):
        self.field_name = field_name
        self.field_value = field_value
        self.index_name = index_name

class UpdateParams:
    def __init__(
        self, 
        document_id: str, 
        updates: Dict[str, Any], 
        condition_field: Optional[str] = None, 
        expected_value: Optional[Any] = None,
        version_field: Optional[str] = None,
        current_version: Optional[int] = None
    ):
        self.document_id = document_id
        self.updates = updates
        self.condition_field = condition_field
        self.expected_value = expected_value
        self.version_field = version_field
        self.current_version = current_version
