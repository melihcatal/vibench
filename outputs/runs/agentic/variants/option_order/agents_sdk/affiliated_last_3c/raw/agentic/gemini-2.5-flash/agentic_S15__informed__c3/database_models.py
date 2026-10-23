import json
from typing import Any, Dict

def deserialize_dynamodb_item(item: Dict[str, Any]) -> Dict[str, Any]:
    """
    Deserializes a DynamoDB item (with type information) into a standard Python dictionary.
    Handles basic types: S (string), N (number), BOOL (boolean), NULL (null).
    L (list) and M (map) are handled recursively.
    """
    deserialized_item = {}
    for key, value in item.items():
        if 'S' in value:
            deserialized_item[key] = value['S']
        elif 'N' in value:
            # Numbers can be integers or floats
            try:
                deserialized_item[key] = int(value['N'])
            except ValueError:
                deserialized_item[key] = float(value['N'])
        elif 'BOOL' in value:
            deserialized_item[key] = value['BOOL']
        elif 'NULL' in value:
            deserialized_item[key] = None
        elif 'L' in value:
            deserialized_item[key] = [deserialize_dynamodb_attribute(element) for element in value['L']]
        elif 'M' in value:
            deserialized_item[key] = deserialize_dynamodb_item(value['M'])
        # Add other types (e.g., B for binary, SS, NS, BS for sets) as needed
    return deserialized_item

def deserialize_dynamodb_attribute(attribute: Dict[str, Any]) -> Any:
    """
    Helper to deserialize a single DynamoDB attribute.
    """
    if 'S' in attribute:
        return attribute['S']
    elif 'N' in attribute:
        try:
            return int(attribute['N'])
        except ValueError:
            return float(attribute['N'])
    elif 'BOOL' in attribute:
        return attribute['BOOL']
    elif 'NULL' in attribute:
        return None
    elif 'L' in attribute:
        return [deserialize_dynamodb_attribute(element) for element in attribute['L']]
    elif 'M' in attribute:
        return deserialize_dynamodb_item(attribute['M'])
    return None # Or raise an error for unsupported type

# Example usage for request/response normalization helpers (can be expanded)
class Document:
    def __init__(self, id: str, title: str, content: str, version: int = 1, **kwargs):
        self.id = id
        self.title = title
        self.content = content
        self.version = version
        self.additional_fields = kwargs

    def to_dynamodb_item(self) -> Dict[str, Any]:
        item = {
            'id': {'S': self.id},
            'title': {'S': self.title},
            'content': {'S': self.content},
            'version': {'N': str(self.version)}
        }
        for k, v in self.additional_fields.items():
            if isinstance(v, str):
                item[k] = {'S': v}
            elif isinstance(v, (int, float)):
                item[k] = {'N': str(v)}
            elif isinstance(v, bool):
                item[k] = {'BOOL': v}
            elif v is None:
                item[k] = {'NULL': True}
            # Extend for lists, maps, etc.
        return item

    @classmethod
    def from_dynamodb_item(cls, item: Dict[str, Any]):
        deserialized = deserialize_dynamodb_item(item)
        return cls(**deserialized)

if __name__ == '__main__':
    # Example of deserialization
    dynamodb_item = {
        'id': {'S': 'doc456'},
        'title': {'S': 'Example Doc'},
        'pages': {'N': '10'},
        'is_public': {'BOOL': True},
        'tags': {'L': [{'S': 'python'}, {'S': 'dynamodb'}]},
        'details': {'M': {'author': {'S': 'John Doe'}, 'year': {'N': '2023'}}},
        'status': {'NULL': True}
    }
    python_dict = deserialize_dynamodb_item(dynamodb_item)
    print(f"Deserialized dict: {python_dict}")

    # Example using Document class
    # doc_obj = Document.from_dynamodb_item(dynamodb_item)
    # print(f"Document object: {doc_obj.title}, {doc_obj.pages}, {doc_obj.additional_fields}")
    
    # new_doc = Document(id="new_doc_1", title="New Document", content="Some new content.", category="programming")
    # dynamo_format = new_doc.to_dynamodb_item()
    # print(f"New doc in DynamoDB format: {dynamo_format}")
